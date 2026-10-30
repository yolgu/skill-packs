# Defense-in-Depth Validation

## Overview

When you fix a bug caused by invalid data, adding validation at one place feels sufficient. But that single check can be bypassed by different code paths, refactoring, or mocks.

**Core principle:** After finding the root cause, validate the value once at the trust boundary where it enters, guarantee each invariant once in the layer that owns it, and do not repeat the same check at every internal call. Make the bug structurally impossible through ownership, not through repetition.

## Why Not Every Layer

Repeating the same check in entry, business, and infrastructure code does not make the bug more impossible. It makes three copies of one rule that drift apart and hide which one is authoritative. What closes the bypass paths is placing each check where it is owned:

- The trust boundary (API input, file, environment, message) validates untrusted input once.
- The layer that owns an invariant enforces it once, in the constructor or method that creates the state, so no code path can build an invalid value.
- Tests isolate dangerous operations on the test side instead of adding environment branches to production code.
- Diagnostic instrumentation follows the cleanup rule in SKILL.md (DEBUG or TRACE on a per-class logger, switched by configuration).

## The Three Placements

### Placement 1: Trust Boundary Validation
**Purpose:** Reject invalid input once, where it enters the system

```typescript
function createProject(name: string, workingDirectory: string): Project {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
  // ... proceed
}
```

### Placement 2: Owner-Enforced Invariant
**Purpose:** Make the invalid state impossible to construct, so inner callers rely on the invariant instead of rechecking it

```typescript
class WorkspaceRoot {
  private constructor(readonly path: string) {}

  static of(path: string): WorkspaceRoot {
    if (!path) {
      throw new Error('workspace root path is required');
    }
    return new WorkspaceRoot(path);
  }
}

function initializeWorkspace(root: WorkspaceRoot, sessionId: string): void {
  // root is valid by construction; no second check here
}
```

### Placement 3: Test-Side Isolation
**Purpose:** Keep dangerous real operations (files, git, network) away from the real environment during tests, without an environment branch in production code

```typescript
// test setup: give the code under test a temp directory and a recording fake
const tempDir: string = mkdtempSync(join(tmpdir(), 'workspace-'));
const git: RecordingGit = new RecordingGit();
const manager: WorktreeManager = new WorktreeManager(WorkspaceRoot.of(tempDir), git);
```

Production code does not inspect the environment to decide whether it is running in a test.

## Applying the Pattern

When you find a bug:

1. **Trace the data flow** - Where does the bad value originate? Where is it used?
2. **Find the trust boundary** - The first place the value enters from outside; validate it there once.
3. **Find the owner** - The type or method that creates the state; enforce the invariant there once.
4. **Isolate on the test side** - Temp directories, injected fakes, configuration; no environment branches in production code.
5. **Test the boundary and the owner** - One test proves the boundary rejects bad input; one proves the owner cannot be built invalid.

## Example from Session

Bug: Empty `projectDir` caused `git init` in source code

**Data flow:**
1. Test setup → empty string
2. `Project.create(name, '')`
3. `WorkspaceManager.createWorkspace('')`
4. `git init` runs in `process.cwd()`

**Placements:**
- Trust boundary: `Project.create()` validates not empty/exists/writable
- Owner: the workspace root type cannot be constructed from an empty path, so `WorkspaceManager` relies on it instead of rechecking
- Test side: tests give `WorktreeManager` a temp directory and a recording git fake, so a regression cannot touch the real repository

**Result:** The bug cannot recur through another code path, because no path can build an empty workspace root.

## Key Insight

The bypasses that defeat a single check (other code paths, mocks, refactoring) are closed by ownership, not by repetition. An invariant enforced where the state is created holds on every path, and a check at the trust boundary covers every entry. **Validate once where the value enters, enforce once where it is owned, and keep test safety in the tests.**
