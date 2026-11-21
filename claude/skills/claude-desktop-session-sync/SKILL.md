---
name: claude-desktop-session-sync
description: "Bring Claude desktop Code-tab sessions across when the user switches between two Claude accounts on the same Mac, so the session sidebar of the account they are moving to shows the sessions from the other one. Use it when the user says the sessions are gone after changing accounts, or asks to copy, move or sync sessions between accounts, for example '계정 바꿨더니 세션이 안 보여', '세션 목록 옮겨줘', '다른 계정에 있는 세션 가져와'. Not for conversations on claude.ai, and not for moving sessions to another computer."
---

# Claude desktop session sync between accounts

The Claude desktop app keeps the Code-tab session sidebar per account. After the user signs in with another account the sidebar looks empty, although every conversation is still on disk. There is no built-in way to carry the sidebar across accounts: the app's own session import only covers other organizations of the same account. This procedure copies the sidebar entries between the two account folders. It relies on how the app stores them, which is not documented and can change; the layout below was last checked on 2026-11-16.

## Where things are

- Sidebar entries: `~/Library/Application Support/Claude/claude-code-sessions/<account id>/<organization id>/local_*.json`, one file per session.
- The conversation itself: `~/.claude/projects/<project folder>/<cliSessionId>.jsonl`. It does not depend on the account, so both accounts open the same conversation.
- The account the app is signed in to: `lastKnownAccountUuid` in `~/Library/Application Support/Claude/config.json`. Do not take it from `~/.claude.json`, which can name a different account.
- Sidebar groups and pins are not in these files and do not come across.

Find the two account folders by listing `claude-code-sessions/`; the one whose name matches `lastKnownAccountUuid` is the destination when the user has already switched. If it is unclear which folder is which, ask. Do not write account ids or email addresses into any file while doing this.

## Steps

1. Confirm the direction with the user: which account's sessions go to which.
2. Back up the destination folder's `local_*.json` files before changing anything, into `~/Library/Application Support/Claude/claude-code-sessions-backup/<date>-<destination>-before-sync/`.
3. Entry only in the source: copy it, keeping timestamps (`cp -p`). Archived sessions keep their `isArchived` value.
4. Entry in both: compare `lastActivityAt`. The copy with the later value replaces the other. Entries that differ only in `lastFocusedAt` or snapshot fields do not need replacing.
5. Copy only `local_*.json`. Leave `deleted_*` markers, `scheduled-tasks.json` and every other file in the folder alone.
6. Ask the user to restart the app. The entries appear after the restart.
7. Report how many entries were copied, how many were replaced, and where the backup is.

## Why the later copy must win

An entry is more than sidebar metadata. Its `cliSessionId` can change when the app moves a session to a new conversation file, so an older copy of the same entry can reopen an earlier conversation. Replacing only when the other side has the later `lastActivityAt` keeps the entry that points at the conversation the user worked in last.
