#Requires -Version 5.1
<#
.SYNOPSIS
    Moves Claude desktop app Code-tab sessions from one account store to another.

.DESCRIPTION
    The desktop app keeps one metadata file per Code-tab session at
        <DataRoot>\claude-code-sessions\<accountUuid>\<orgUuid>\local_<id>.json
    and an account's sidebar lists only the files in its own folder, called a store here.
    Conversation transcripts live in the shared <ConfigDir>\projects folder, keyed by the
    session's working folder, so they never belong to an account.

    Moving a session therefore means:
      * moving its metadata file into the target store,
      * carrying its entry in the store's archive index, and
      * for a session started without a project folder, moving its scratch folder (which
        sits under the source account's path) together with the transcript folder named
        after it, and rewriting those paths inside the metadata file.

    The running app keeps its session list in memory and does not notice moved files.
    Restart it completely after a move. Moving the sessions back reverses a move.

.EXAMPLE
    .\Move-Sessions.ps1 -List
    Lists every store on this computer with its session count and recent titles.

.EXAMPLE
    .\Move-Sessions.ps1 -List -From current
    Lists the sessions of the store the calling app session runs in.

.EXAMPLE
    .\Move-Sessions.ps1 -From <accountUuid>/<orgUuid> -To current -DryRun
    Prints what would move and what would be skipped, without changing anything.
#>
[CmdletBinding()]
param(
    [switch] $List,
    [string] $From,
    [string] $To,
    [string[]] $SessionId = @(),
    [string[]] $Exclude = @(),
    [switch] $DryRun,
    [string] $DataRoot,
    [string] $ConfigDir
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

class SessionRecord {
    [string] $LocalId
    [string] $CliSessionId
    [string] $Title
    [string] $Cwd
    [bool] $IsArchived
    [datetime] $LastActivity
    [string] $MetadataPath

    static [SessionRecord] Read([string] $metadataPath) {
        $json = [System.IO.File]::ReadAllText($metadataPath, [System.Text.Encoding]::UTF8) | ConvertFrom-Json
        $record = [SessionRecord]::new()
        $record.MetadataPath = $metadataPath
        # The app names the file after the session, so the file name is the id that file moves act on.
        $record.LocalId = [System.IO.Path]::GetFileNameWithoutExtension($metadataPath)
        $record.CliSessionId = [string][SessionRecord]::OptionalField($json, 'cliSessionId')
        $storedTitle = [SessionRecord]::OptionalField($json, 'title')
        $record.Title = if ($storedTitle) { [string]$storedTitle } else { '(untitled)' }
        $record.Cwd = [string][SessionRecord]::OptionalField($json, 'cwd')
        $record.IsArchived = [bool][SessionRecord]::OptionalField($json, 'isArchived')
        $record.LastActivity = [SessionRecord]::ActivityTime($json)
        return $record
    }

    hidden static [object] OptionalField([psobject] $json, [string] $name) {
        $property = $json.PSObject.Properties[$name]
        if ($null -eq $property) { return $null }
        return $property.Value
    }

    hidden static [datetime] ActivityTime([psobject] $json) {
        foreach ($name in @('lastActivityAt', 'createdAt')) {
            $epochMilliseconds = [SessionRecord]::OptionalField($json, $name)
            if ($null -ne $epochMilliseconds) {
                return [DateTimeOffset]::FromUnixTimeMilliseconds([long]$epochMilliseconds).LocalDateTime
            }
        }
        return [datetime]::MinValue
    }
}

class SessionStore {
    [string] $AccountUuid
    [string] $OrgUuid
    [string] $SessionsDir
    [string] $ScratchDir
    [bool] $IsCurrent

    SessionStore([string] $dataRoot, [string] $accountUuid, [string] $orgUuid, [bool] $isCurrent) {
        $this.AccountUuid = $accountUuid
        $this.OrgUuid = $orgUuid
        $this.SessionsDir = [System.IO.Path]::Combine($dataRoot, 'claude-code-sessions', $accountUuid, $orgUuid)
        $this.ScratchDir = [System.IO.Path]::Combine($dataRoot, 'scratch-workspaces', $accountUuid, $orgUuid)
        $this.IsCurrent = $isCurrent
    }

    [string] Key() {
        return "$($this.AccountUuid)/$($this.OrgUuid)"
    }

    [SessionRecord[]] ReadSessions() {
        $records = foreach ($file in Get-ChildItem -LiteralPath $this.SessionsDir -Filter 'local_*.json' -File) {
            [SessionRecord]::Read($file.FullName)
        }
        return @($records | Sort-Object -Property LastActivity -Descending)
    }

    [string] MetadataPathFor([string] $localId) {
        return Join-Path $this.SessionsDir "$localId.json"
    }

    [bool] HoldsScratchPath([string] $path) {
        return $path.StartsWith($this.ScratchDir + '\', [System.StringComparison]::OrdinalIgnoreCase)
    }

    # The scratch folder is the direct child of the store's scratch root that contains the path.
    [string] ScratchFolderOf([string] $path) {
        $relative = $path.Substring($this.ScratchDir.Length + 1)
        return Join-Path $this.ScratchDir $relative.Split('\')[0]
    }

    [string] ArchiveIndexPath() {
        return Join-Path $this.SessionsDir 'archived-sessions.idx'
    }

    [psobject] ReadArchiveIndex() {
        $indexPath = $this.ArchiveIndexPath()
        if (Test-Path -LiteralPath $indexPath) {
            return [System.IO.File]::ReadAllText($indexPath, [System.Text.Encoding]::UTF8) | ConvertFrom-Json
        }
        return [pscustomobject]@{ v = 1; archived = @() }
    }

    [void] WriteArchiveIndex([psobject] $index) {
        $text = ConvertTo-Json -InputObject $index -Compress -Depth 5
        [System.IO.File]::WriteAllText($this.ArchiveIndexPath(), $text, [System.Text.UTF8Encoding]::new($false))
    }
}

class ClaudeDataLayout {
    [string] $DataRoot
    [string] $ProjectsDir
    [string] $BackupRoot
    [string] $CurrentAccountUuid
    [string] $CurrentOrgUuid
    [string] $CurrentSessionId

    # The desktop app passes the calling session's account, organization, and session ids
    # to every Code-tab session through these environment variables.
    ClaudeDataLayout([string] $dataRoot, [string] $configDir) {
        $this.DataRoot = $dataRoot
        $this.ProjectsDir = Join-Path $configDir 'projects'
        $this.BackupRoot = Join-Path $configDir 'session-account-move-backups'
        $this.CurrentAccountUuid = [string]$env:CLAUDE_CODE_ACCOUNT_UUID
        $this.CurrentOrgUuid = [string]$env:CLAUDE_CODE_ORGANIZATION_UUID
        $this.CurrentSessionId = [string]$env:CLAUDE_CODE_HOST_SESSION_ID
    }

    [SessionStore[]] ListStores() {
        $root = Join-Path $this.DataRoot 'claude-code-sessions'
        $stores = foreach ($account in Get-ChildItem -LiteralPath $root -Directory) {
            foreach ($org in Get-ChildItem -LiteralPath $account.FullName -Directory) {
                $isCurrent = ($account.Name -eq $this.CurrentAccountUuid) -and ($org.Name -eq $this.CurrentOrgUuid)
                [SessionStore]::new($this.DataRoot, $account.Name, $org.Name, $isCurrent)
            }
        }
        return @($stores)
    }

    [SessionStore] ResolveStore([string] $spec) {
        $key = $spec
        if ($spec -eq 'current') {
            if (-not $this.CurrentAccountUuid -or -not $this.CurrentOrgUuid) {
                throw "'current' works only inside a desktop app session. Pass <accountUuid>/<orgUuid> instead."
            }
            $key = "$($this.CurrentAccountUuid)/$($this.CurrentOrgUuid)"
        }
        $found = @($this.ListStores() | Where-Object { $_.Key() -eq $key })
        if ($found.Count -ne 1) {
            throw "No session store '$key' on this computer. Run with -List to see the stores."
        }
        return $found[0]
    }

    # Claude Code names a transcript folder after the working folder, with every
    # character other than an ASCII letter or digit replaced by '-'.
    [string] TranscriptDirFor([string] $cwd) {
        return Join-Path $this.ProjectsDir ($cwd -replace '[^A-Za-z0-9]', '-')
    }
}

class ScratchRelocation {
    [string] $FromFolder
    [string] $ToFolder
    [string] $BlockedReason = ''
    [System.Collections.Generic.Dictionary[string, string]] $TranscriptDirs = [System.Collections.Generic.Dictionary[string, string]]::new()

    [string] Relocate([string] $path) {
        return $this.ToFolder + $path.Substring($this.FromFolder.Length)
    }
}

class SessionMove {
    [SessionRecord] $Session
    [string] $TargetPath
    [ScratchRelocation] $Scratch
}

class SessionSkip {
    [SessionRecord] $Session
    [string] $Reason
}

class MovePlan {
    [SessionStore] $From
    [SessionStore] $To
    [System.Collections.Generic.List[SessionMove]] $Moves = [System.Collections.Generic.List[SessionMove]]::new()
    [System.Collections.Generic.List[SessionSkip]] $Skips = [System.Collections.Generic.List[SessionSkip]]::new()
    [System.Collections.Generic.List[ScratchRelocation]] $Relocations = [System.Collections.Generic.List[ScratchRelocation]]::new()

    static [MovePlan] Build([ClaudeDataLayout] $layout, [SessionStore] $from, [SessionStore] $to, [string[]] $requestedIds, [string[]] $excludedIds) {
        if ($from.Key() -eq $to.Key()) {
            throw 'The source and target stores are the same.'
        }
        $plan = [MovePlan]::new()
        $plan.From = $from
        $plan.To = $to

        $storeSessions = $from.ReadSessions()
        $excluded = @(@($excludedIds) + @($layout.CurrentSessionId) | Where-Object { $_ } | ForEach-Object { [MovePlan]::NormalizeId($_) })
        $candidates = [System.Collections.Generic.List[SessionRecord]]::new()
        foreach ($session in [MovePlan]::SelectRequested($storeSessions, $requestedIds)) {
            if ($excluded -contains $session.LocalId) {
                $plan.AddSkip($session, 'excluded: it is the session running this move, or it was listed in -Exclude')
            }
            elseif (Test-Path -LiteralPath $to.MetadataPathFor($session.LocalId)) {
                $plan.AddSkip($session, 'the target store already has a session with this id')
            }
            else {
                $candidates.Add($session)
            }
        }

        $relocationByFolder = @{}
        foreach ($session in $candidates) {
            if (-not $from.HoldsScratchPath($session.Cwd)) {
                $plan.AddMove($session, $null)
                continue
            }
            $folder = $from.ScratchFolderOf($session.Cwd)
            if (-not $relocationByFolder.ContainsKey($folder)) {
                $relocation = [MovePlan]::PlanScratch($layout, $from, $to, $folder, $storeSessions, $candidates)
                $relocationByFolder[$folder] = $relocation
                if (-not $relocation.BlockedReason) { $plan.Relocations.Add($relocation) }
            }
            $relocation = $relocationByFolder[$folder]
            if ($relocation.BlockedReason) { $plan.AddSkip($session, $relocation.BlockedReason) }
            else { $plan.AddMove($session, $relocation) }
        }
        return $plan
    }

    [void] AddMove([SessionRecord] $session, [ScratchRelocation] $scratch) {
        $move = [SessionMove]::new()
        $move.Session = $session
        $move.TargetPath = $this.To.MetadataPathFor($session.LocalId)
        $move.Scratch = $scratch
        $this.Moves.Add($move)
    }

    [void] AddSkip([SessionRecord] $session, [string] $reason) {
        $skip = [SessionSkip]::new()
        $skip.Session = $session
        $skip.Reason = $reason
        $this.Skips.Add($skip)
    }

    hidden static [SessionRecord[]] SelectRequested([SessionRecord[]] $sessions, [string[]] $requestedIds) {
        if (@($requestedIds).Count -eq 0) { return $sessions }
        $storeIds = @($sessions | ForEach-Object { $_.LocalId })
        $wanted = @($requestedIds | ForEach-Object { [MovePlan]::NormalizeId($_) })
        $unknown = @($wanted | Where-Object { $storeIds -notcontains $_ })
        if ($unknown.Count -gt 0) {
            throw "Not in the source store: $($unknown -join ', ')"
        }
        return @($sessions | Where-Object { $wanted -contains $_.LocalId })
    }

    hidden static [string] NormalizeId([string] $id) {
        $trimmed = $id.Trim()
        if ($trimmed.StartsWith('local_')) { return $trimmed }
        return "local_$trimmed"
    }

    # A scratch folder and its transcript folders move as one unit, so every session that
    # works in the folder has to move with it.
    hidden static [ScratchRelocation] PlanScratch([ClaudeDataLayout] $layout, [SessionStore] $from, [SessionStore] $to, [string] $folder, [SessionRecord[]] $storeSessions, [System.Collections.Generic.List[SessionRecord]] $candidates) {
        $relocation = [ScratchRelocation]::new()
        $relocation.FromFolder = $folder
        $relocation.ToFolder = Join-Path $to.ScratchDir (Split-Path $folder -Leaf)

        $members = @($storeSessions | Where-Object { $from.HoldsScratchPath($_.Cwd) -and ($from.ScratchFolderOf($_.Cwd) -eq $folder) })
        $movingIds = @($candidates | ForEach-Object { $_.LocalId })
        $stayingIds = @($members | Where-Object { $movingIds -notcontains $_.LocalId } | ForEach-Object { $_.LocalId })
        if ($stayingIds.Count -gt 0) {
            $relocation.BlockedReason = "its scratch folder is shared with sessions that are not moving ($($stayingIds -join ', ')); move them together"
            return $relocation
        }
        if (-not (Test-Path -LiteralPath $folder)) {
            $relocation.BlockedReason = "its scratch folder no longer exists: $folder"
            return $relocation
        }
        if (Test-Path -LiteralPath $relocation.ToFolder) {
            $relocation.BlockedReason = "the target already has a scratch folder with this name: $($relocation.ToFolder)"
            return $relocation
        }
        foreach ($cwd in @($members | ForEach-Object { $_.Cwd } | Select-Object -Unique)) {
            $fromTranscriptDir = $layout.TranscriptDirFor($cwd)
            $toTranscriptDir = $layout.TranscriptDirFor($relocation.Relocate($cwd))
            $withoutTranscript = @($members | Where-Object { ($_.Cwd -eq $cwd) -and -not (Test-Path -LiteralPath (Join-Path $fromTranscriptDir "$($_.CliSessionId).jsonl")) })
            if ($withoutTranscript.Count -gt 0) {
                $relocation.BlockedReason = "its transcript is not where the scratch folder name points: $fromTranscriptDir"
                return $relocation
            }
            if (Test-Path -LiteralPath $toTranscriptDir) {
                $relocation.BlockedReason = "the target transcript folder already exists: $toTranscriptDir"
                return $relocation
            }
            $relocation.TranscriptDirs[$fromTranscriptDir] = $toTranscriptDir
        }
        return $relocation
    }
}

function Resolve-DataRoot {
    [OutputType([string])]
    param([string] $Requested)

    if ($Requested) { return (Resolve-Path -LiteralPath $Requested).Path }
    $appDataParent = Join-Path $env:LOCALAPPDATA 'Claude-Data'
    $found = @(Get-ChildItem -LiteralPath $appDataParent -Directory -Filter 'claude_*' -ErrorAction SilentlyContinue |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'claude-code-sessions') })
    if ($found.Count -ne 1) {
        throw "Found $($found.Count) desktop app data folders under $appDataParent. Pass -DataRoot."
    }
    return $found[0].FullName
}

# Under `powershell -File` an array parameter arrives as one comma-joined string, so ids
# are accepted in either form. The leading comma keeps an empty list an empty array:
# otherwise the function emits nothing and the caller receives $null.
function Split-IdList {
    [OutputType([string[]])]
    param([string[]] $Ids)

    return , [string[]]@($Ids | ForEach-Object { $_ -split '[,\s]+' } | Where-Object { $_ })
}

function Resolve-ConfigDir {
    [OutputType([string])]
    param([string] $Requested)

    if ($Requested) { return (Resolve-Path -LiteralPath $Requested).Path }
    if ($env:CLAUDE_CONFIG_DIR) { return $env:CLAUDE_CONFIG_DIR }
    return Join-Path $HOME '.claude'
}

function Format-SessionLine {
    [OutputType([string])]
    param([SessionRecord] $Session)

    return '{0}  {1}  {2}' -f $Session.LocalId, $Session.LastActivity.ToString('yyyy-MM-dd HH:mm'), $Session.Title
}

function Format-StoreLabel {
    [OutputType([string])]
    param([SessionStore] $Store)

    if ($Store.IsCurrent) { return "$($Store.Key())  [current]" }
    return $Store.Key()
}

function Write-StoreList {
    [OutputType([string])]
    param([ClaudeDataLayout] $Layout)

    $storesById = @{}
    foreach ($store in $Layout.ListStores()) {
        $sessions = $store.ReadSessions()
        Format-StoreLabel $store
        if ($sessions.Count -eq 0) {
            '    no sessions'
            continue
        }
        $archivedCount = @($sessions | Where-Object { $_.IsArchived }).Count
        '    sessions: {0} (archived {1}), last activity {2}' -f $sessions.Count, $archivedCount, $sessions[0].LastActivity.ToString('yyyy-MM-dd HH:mm')
        '    recent: ' + (@($sessions | Select-Object -First 3 | ForEach-Object { $_.Title }) -join ' | ')
        foreach ($session in $sessions) {
            if (-not $storesById.ContainsKey($session.LocalId)) { $storesById[$session.LocalId] = @() }
            $storesById[$session.LocalId] += $store.Key()
        }
    }
    foreach ($entry in $storesById.GetEnumerator()) {
        if (@($entry.Value).Count -gt 1) {
            'WARNING: {0} is in more than one store: {1}' -f $entry.Key, (@($entry.Value) -join ', ')
        }
    }
}

function Write-SessionList {
    [OutputType([string])]
    param([SessionStore] $Store)

    $sessions = $Store.ReadSessions()
    if ($sessions.Count -eq 0) {
        'no sessions in ' + (Format-StoreLabel $Store)
        return
    }
    foreach ($session in $sessions) {
        $place = if ($Store.HoldsScratchPath($session.Cwd)) { '[scratch]' } else { $session.Cwd }
        $archived = if ($session.IsArchived) { '  [archived]' } else { '' }
        '{0}{1}  @ {2}' -f (Format-SessionLine $session), $archived, $place
    }
}

function Write-Plan {
    [OutputType([string])]
    param([MovePlan] $Plan)

    'From: ' + (Format-StoreLabel $Plan.From)
    'To:   ' + (Format-StoreLabel $Plan.To)
    "Sessions to move: $($Plan.Moves.Count)"
    foreach ($move in $Plan.Moves) {
        $scratchNote = if ($move.Scratch) { '  (with its scratch folder)' } else { '' }
        '  ' + (Format-SessionLine $move.Session) + $scratchNote
    }
    if ($Plan.Skips.Count -gt 0) {
        "Sessions skipped: $($Plan.Skips.Count)"
        foreach ($skip in $Plan.Skips) {
            '  ' + (Format-SessionLine $skip.Session) + "  -- $($skip.Reason)"
        }
    }
}

function Save-MoveBackup {
    [OutputType([string])]
    param([ClaudeDataLayout] $Layout, [MovePlan] $Plan)

    $backupDir = Join-Path $Layout.BackupRoot (Get-Date -Format 'yyyyMMdd-HHmmss')
    foreach ($store in @($Plan.From, $Plan.To)) {
        $storeBackupDir = Join-Path $backupDir "$($store.AccountUuid)_$($store.OrgUuid)"
        New-Item -ItemType Directory -Force -Path $storeBackupDir | Out-Null
        if (Test-Path -LiteralPath $store.ArchiveIndexPath()) {
            Copy-Item -LiteralPath $store.ArchiveIndexPath() -Destination $storeBackupDir
        }
    }
    $sourceBackupDir = Join-Path $backupDir "$($Plan.From.AccountUuid)_$($Plan.From.OrgUuid)"
    foreach ($move in $Plan.Moves) {
        Copy-Item -LiteralPath $move.Session.MetadataPath -Destination $sourceBackupDir
    }
    $record = @(Write-Plan $Plan) + @('') + @($Plan.Relocations | ForEach-Object { "scratch: $($_.FromFolder) -> $($_.ToFolder)" })
    [System.IO.File]::WriteAllLines((Join-Path $backupDir 'plan.txt'), [string[]]$record, [System.Text.UTF8Encoding]::new($false))
    return $backupDir
}

function Move-ScratchFolders {
    param([MovePlan] $Plan)

    foreach ($relocation in $Plan.Relocations) {
        New-Item -ItemType Directory -Force -Path (Split-Path $relocation.ToFolder -Parent) | Out-Null
        Move-Item -LiteralPath $relocation.FromFolder -Destination $relocation.ToFolder
        foreach ($transcriptDir in $relocation.TranscriptDirs.GetEnumerator()) {
            Move-Item -LiteralPath $transcriptDir.Key -Destination $transcriptDir.Value
        }
    }
}

# The metadata names the scratch folder both as a JSON-escaped path (cwd and similar fields)
# and through its transcript folder name (for example the memory folder path in the prompt
# snapshot), so both spellings are rewritten.
function Update-ScratchPaths {
    param([SessionMove] $Move, [ClaudeDataLayout] $Layout)

    $relocation = $Move.Scratch
    $text = [System.IO.File]::ReadAllText($Move.TargetPath, [System.Text.Encoding]::UTF8)
    $text = $text.Replace($relocation.FromFolder.Replace('\', '\\'), $relocation.ToFolder.Replace('\', '\\'))
    $fromName = Split-Path $Layout.TranscriptDirFor($relocation.FromFolder) -Leaf
    $toName = Split-Path $Layout.TranscriptDirFor($relocation.ToFolder) -Leaf
    $text = $text.Replace($fromName, $toName)
    [System.IO.File]::WriteAllText($Move.TargetPath, $text, [System.Text.UTF8Encoding]::new($false))
}

function Move-ArchiveMembership {
    param([MovePlan] $Plan)

    $movedIds = @($Plan.Moves | ForEach-Object { $_.Session.LocalId })
    $fromIndex = $Plan.From.ReadArchiveIndex()
    $carriedIds = @(@($fromIndex.archived) | Where-Object { $movedIds -contains $_ })
    if ($carriedIds.Count -eq 0) { return }

    $fromIndex.archived = @(@($fromIndex.archived) | Where-Object { $movedIds -notcontains $_ })
    $Plan.From.WriteArchiveIndex($fromIndex)
    $toIndex = $Plan.To.ReadArchiveIndex()
    $toIndex.archived = @(@($toIndex.archived) + $carriedIds | Select-Object -Unique)
    $Plan.To.WriteArchiveIndex($toIndex)
}

function Invoke-MovePlan {
    [OutputType([string])]
    param([ClaudeDataLayout] $Layout, [MovePlan] $Plan)

    $backupDir = Save-MoveBackup -Layout $Layout -Plan $Plan
    Move-ScratchFolders -Plan $Plan
    foreach ($move in $Plan.Moves) {
        Move-Item -LiteralPath $move.Session.MetadataPath -Destination $move.TargetPath
        if ($move.Scratch) { Update-ScratchPaths -Move $move -Layout $Layout }
    }
    Move-ArchiveMembership -Plan $Plan
    return $backupDir
}

function Test-MovedSessions {
    [OutputType([string])]
    param([MovePlan] $Plan)

    foreach ($move in $Plan.Moves) {
        $moved = [SessionRecord]::Read($move.TargetPath)
        if (Test-Path -LiteralPath $moved.Cwd) {
            '  ok    ' + (Format-SessionLine $moved)
        }
        else {
            '  WARN  ' + (Format-SessionLine $moved) + "  -- working folder not found: $($moved.Cwd)"
        }
    }
}

$layout = [ClaudeDataLayout]::new((Resolve-DataRoot $DataRoot), (Resolve-ConfigDir $ConfigDir))

if ($List) {
    if ($From) { Write-SessionList -Store $layout.ResolveStore($From) }
    else { Write-StoreList -Layout $layout }
    return
}
if (-not $From -or -not $To) {
    throw 'Pass -List, or both -From and -To.'
}

$plan = [MovePlan]::Build($layout, $layout.ResolveStore($From), $layout.ResolveStore($To), (Split-IdList $SessionId), (Split-IdList $Exclude))
Write-Plan -Plan $plan
if ($DryRun -or $plan.Moves.Count -eq 0) { return }

$backupDir = Invoke-MovePlan -Layout $layout -Plan $plan
''
'Moved. Checking the moved sessions:'
Test-MovedSessions -Plan $plan
"Backup of the changed metadata: $backupDir"
'Quit the desktop app completely (tray icon > Quit) and start it again before opening any moved session.'
