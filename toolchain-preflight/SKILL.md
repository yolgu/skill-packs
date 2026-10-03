---
name: toolchain-preflight
description: "빌드, 테스트, 실행 명령(mvn, gradle, fvm flutter, npm, pnpm, uv, python, docker build 등)을 작업 중 처음 실행하기 전에 사용한다. 프로젝트 파일이 요구하는 언어와 도구 버전을 읽고, 그 명령이 실제로 쓸 런타임과 맞는지 확인한 뒤 명령마다 맞는 버전을 지정해 실행한다. Lombok이 만드는 getter, setter, builder를 찾지 못하는 'cannot find symbol', 'Unsupported class file major version', 'release version N not supported', 'ExceptionInInitializerError' 같은 버전 불일치 오류가 났을 때도 코드를 고치기 전에 반드시 사용한다."
---

# 실행 전 도구 버전 확인

빌드나 테스트가 실패하면 코드를 의심하기 전에 "이 명령이 어떤 런타임으로 돌았는가"부터 확인한다. 같은 Mac에서도 셸의 `java`, Maven이 쓰는 Java, Docker 빌드 이미지의 Java가 서로 다를 수 있다. 여러 에이전트가 이 차이를 모르고 코드 문제로 오해해 시간을 썼다.

## 언제 하는가

- 작업에서 빌드, 테스트, 실행 명령을 처음 실행하기 전에 한 번 한다.
- 다른 저장소로 옮겨 가거나 다른 생태계의 명령(예: Maven 다음 Flutter)을 처음 실행할 때 다시 한다.
- 위 설명의 버전 불일치 오류가 나면 바로 한다.

## 절차

1. **로컬 실행 환경의 규칙을 먼저 읽는다.** 프로젝트나 상위 작업 공간에 `LOCAL-MACHINE.md` 같은 로컬 실행 환경 문서가 있거나 프로젝트 지침이 해당 문서를 가리키면 "빌드" 항목을 읽는다. 그 환경에서 어떤 버전을 어떻게 지정하는지는 해당 문서가 원본이다. 이 스킬에 같은 내용을 옮겨 적지 않는다.

2. **요구 버전과 실제 버전을 함께 본다.**
   ```bash
   bash <이 스킬 경로>/scripts/detect_toolchain.sh <프로젝트 폴더>
   ```
   스크립트는 프로젝트 선언과 현재 셸이 실행할 런타임, 설치된 JDK를 나란히 보여 준다. 스크립트를 쓸 수 없으면 아래를 직접 확인한다.
   - **Maven**: `pom.xml`의 `java.version`, `maven.compiler.release`, `source`, `target`, Spring Boot parent와 Lombok 버전, `Dockerfile`의 빌드 이미지
   - **Gradle**: toolchain `languageVersion`, wrapper의 Gradle 버전
   - **Flutter**: `.fvmrc`나 `.fvm/fvm_config.json`, `pubspec.yaml`의 SDK 범위
   - **Node**: `.nvmrc`, `.node-version`, `package.json`의 `engines`와 `packageManager`
   - **Python**: `.python-version`, `pyproject.toml`의 `requires-python`, `uv.lock`
   - **공통**: `.tool-versions`, `.sdkmanrc`, `.java-version`

3. **명령 자신이 보고하는 버전을 믿는다.** 다른 명령의 결과로 추측하지 않는다.
   - Maven은 `mvn -v`의 `Java version` 줄을 본다. `java -version`이 17이어도 Maven은 다른 JDK로 돌 수 있다.
   - Gradle은 `./gradlew -v`의 JVM 줄을 본다.
   - Flutter는 `fvm flutter --version`을 본다.

4. **맞지 않으면 그 명령에만 버전을 지정한다.**
   ```bash
   JAVA_HOME="$(/usr/libexec/java_home -v 17)" mvn -q -DskipTests compile
   ```
   - 요구 버전이 설치돼 있으면 그 버전을 쓴다.
   - 없으면, 설치된 버전 중 요구 버전 이상이면서 프로젝트의 annotation processor와 플러그인이 지원하는 가장 낮은 버전을 쓴다. 예를 들어 Lombok 1.18.22와 Spring Boot 2.6은 JDK 17까지 지원한다.
   - 맞는 버전이 없으면 멈추고 보고한다. 설치와 전역 설정 변경(`~/.mavenrc`, 셸 프로필, `brew link`)은 사용자 승인 없이 하지 않는다.

5. **환경 때문에 프로젝트 파일을 고치지 않는다.** `pom.xml`의 Java 버전, Lombok 버전, wrapper를 바꿔서 로컬 환경에 맞추지 않는다. 그런 변경은 운영 빌드에 영향을 주는 별도 결정이다.

6. **보고에 실제로 쓴 런타임을 적는다.** 로컬 런타임이 운영 빌드 이미지와 다르면 그 차이도 적는다.
   > Java 17로 컴파일했습니다. 운영 이미지는 JDK 11입니다.

## 오류로 원인 찾기

| 증상 | 흔한 원인 | 조치 |
|---|---|---|
| Lombok 클래스의 `getX()`, `setX()`, `builder()`, `log`에 `cannot find symbol` | JDK가 Lombok보다 새로워 annotation processor가 동작하지 않음 | 지원 JDK로 같은 명령 재실행 |
| `Fatal error compiling: java.lang.ExceptionInInitializerError` (javac 내부) | 위와 같음(Lombok과 javac 내부 API 불일치) | 위와 같음 |
| `Unsupported class file major version NN` | 플러그인이나 Gradle이 실행 JDK보다 오래됨 | 더 낮은 JDK로 실행 |
| `release version N not supported`, `invalid target release` | 실행 JDK가 대상 버전보다 오래됨 | 더 높은 JDK로 실행 |
| `The current Dart SDK version is ...` | 고정되지 않은 Flutter로 실행 | `fvm flutter`로 실행 |
| `engine "node" is incompatible` | Node 버전 불일치 | 선언된 Node로 실행 |

환경을 고친 뒤에는 같은 명령을 그대로 다시 실행해 결과를 비교한다.

증분 빌드는 이전 산출물을 재사용해서 잘못된 JDK로도 통과한 것처럼 보일 수 있다. JDK 문제를 판단할 때는 다음 둘 중 하나로 확인한다.
- 깨끗한 빌드(`clean compile`)
- 새 체크아웃에서 컴파일
