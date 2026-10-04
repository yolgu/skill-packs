# skill-packs

Claude Code와 Codex가 함께 쓰는 스킬, 전역 지침, 서브에이전트 정의를 한곳에서 관리하는 저장소입니다. 스킬 본문은 한 벌만 두고, 하네스마다 다른 부분은 얇은 설정 층으로만 나눕니다. [superpowers](https://github.com/obra/superpowers)의 구성 방식을 따랐습니다.

## 구조

```
common/skills/<스킬>/     두 하네스가 같이 쓰는 스킬
  SKILL.md                본문과 Claude Code 설정(머리말)
  agents/openai.yaml      Codex 설정(표시 이름, 자동 호출 여부)
claude/
  CLAUDE.md               Claude Code 전역 지침
  agents/*.md             Claude Code 서브에이전트 정의
codex/
  AGENTS.md               Codex 전역 지침
  agents/*.toml           Codex 서브에이전트 정의
  skills/<스킬>/          Codex에서만 쓰는 스킬
scripts/install.sh        각 하네스가 읽는 위치에 링크를 만든다
```

## 설치

```bash
git clone https://github.com/yolgu/skill-packs.git ~/Documents/projects/skill-packs
~/Documents/projects/skill-packs/scripts/install.sh
```

설치 스크립트는 파일을 복사하지 않고 링크를 만듭니다. 저장소에서 고친 내용이 두 하네스에 바로 반영됩니다.

| 하네스 | 전역 지침 | 서브에이전트 | 스킬 |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/agents` | `~/.claude/skills/<스킬>` ← `common`, `claude` |
| Codex | `~/.codex/AGENTS.md` | `~/.codex/agents` | `~/.agents/skills/<스킬>` ← `common`, `codex` |

- 한 하네스만 설치하려면 `install.sh claude` 또는 `install.sh codex`로 실행합니다.
- 연결 위치에 링크가 아닌 실제 파일이나 폴더가 있으면 덮어쓰지 않고 건너뜁니다. 그 항목을 옮긴 뒤 다시 실행합니다.
- 스킬을 추가하거나 이름을 바꾸면 다시 실행합니다. 저장소에서 빠진 스킬의 링크는 이때 정리됩니다.
- Codex 스킬은 Codex의 현재 사용자 스킬 위치인 `~/.agents/skills`에 연결합니다. `~/.codex/skills`는 Codex가 하위 호환용으로만 읽는 옛 위치이고, 지금은 Codex가 직접 관리하는 시스템 스킬(`.system`)만 남아 있습니다.

## 스킬을 두는 곳

- 기본은 `common/skills`입니다. 한 하네스에서만 의미가 있는 스킬만 `claude/skills`나 `codex/skills`에 둡니다.
- 본문에는 특정 하네스의 도구 이름이나 호출 표기(`/이름`, `$이름`) 대신 동작을 씁니다. 하네스마다 달라야 하는 내용은 하네스 이름으로 항목을 나눠 적습니다. 예: `using-superpowers`의 Platform Adaptation, `subagent-delegation-guard`의 Runtime Mapping.

## 하네스별 설정

각 하네스는 자기 설정만 읽고 다른 하네스의 설정은 무시합니다. 그래서 한 스킬 폴더에 두 설정을 함께 둡니다.

| 설정 | Claude Code | Codex |
| --- | --- | --- |
| 자동 호출 막기 | `SKILL.md` 머리말의 `disable-model-invocation: true` | `agents/openai.yaml`의 `policy.allow_implicit_invocation: false` |
| 표시 이름, 기본 프롬프트 | 없음 | `agents/openai.yaml`의 `interface` |

자동 호출 여부는 하네스마다 다르게 둘 수 있습니다. 예를 들어 `create-prd`는 Claude Code에서는 자동으로 고를 수 있고, Codex에서는 직접 불렀을 때만 씁니다.

## 이 저장소에 넣지 않는 것

이 저장소는 공개 저장소입니다. 다음 항목은 각 컴퓨터에만 둡니다.

- 프로젝트 전용 스킬(`jentrip-*` 등): 각 하네스의 스킬 폴더(`~/.claude/skills`, `~/.agents/skills`)에 실제 폴더로 둡니다. 설치 스크립트는 실제 폴더를 건드리지 않습니다.
- 컴퓨터별 규칙 문서: 작업 폴더 상위의 `CLAUDE.md`나 `AGENTS.md`에 둡니다.
- Codex 시스템 스킬(`~/.codex/skills/.system`): Codex에 내장된 시스템 스킬이 바뀌면 Codex가 이 폴더를 지우고 다시 씁니다.
