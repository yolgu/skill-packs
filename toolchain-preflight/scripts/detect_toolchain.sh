#!/usr/bin/env bash
# Show what a project asks for (toolchain declarations) next to what the shell
# will actually run, so the right runtime can be chosen before building.
# Usage: detect_toolchain.sh [project_dir]
set -u

project_dir="${1:-.}"
cd "$project_dir" || exit 1

print_file_matches() {
  local file="$1"
  local pattern="$2"
  [ -f "$file" ] || return 0
  grep -n -E "$pattern" "$file" 2>/dev/null | head -5 | sed "s#^#  $file:#"
}

print_file_content() {
  local file="$1"
  [ -f "$file" ] || return 0
  echo "  $file: $(tr '\n' ' ' < "$file" | cut -c1-200)"
}

echo "## Declared by the project ($(pwd))"
print_file_matches pom.xml '<java.version>|<maven.compiler.(release|source|target)>|<release>|spring-boot-starter-parent|<artifactId>lombok'
if [ -f pom.xml ] && grep -q '<artifactId>lombok' pom.xml; then
  grep -A2 '<artifactId>lombok' pom.xml | grep -m1 -o '<version>[^<]*' | sed 's#<version>#  lombok version: #'
fi
for gradle_file in build.gradle build.gradle.kts; do
  print_file_matches "$gradle_file" 'languageVersion|sourceCompatibility|targetCompatibility|jvmTarget'
done
print_file_matches gradle/wrapper/gradle-wrapper.properties 'distributionUrl'
for docker_file in Dockerfile Dockerfile.*; do
  print_file_matches "$docker_file" '^FROM '
done
for version_file in .java-version .sdkmanrc .tool-versions .nvmrc .node-version .python-version .fvmrc .fvm/fvm_config.json; do
  print_file_content "$version_file"
done
print_file_matches package.json '"engines"|"node"|"packageManager"'
print_file_matches pyproject.toml 'requires-python'
print_file_matches pubspec.yaml '^  sdk:|^  flutter:'

echo
echo "## What the shell will run"
echo "  JAVA_HOME=${JAVA_HOME:-<unset>}"
if command -v java >/dev/null 2>&1; then
  echo "  java: $(java -version 2>&1 | head -1)"
fi
if [ -f pom.xml ] && command -v mvn >/dev/null 2>&1; then
  echo "  mvn: $(mvn -v 2>/dev/null | grep -m1 'Java version')"
fi
if [ -x /usr/libexec/java_home ]; then
  echo "  installed JDKs (java_home):"
  /usr/libexec/java_home -V 2>&1 | grep -E '^ +[0-9]' | sed 's#^ *#    #'
fi
if command -v brew >/dev/null 2>&1; then
  brew_jdks="$(ls "$(brew --prefix)/opt" 2>/dev/null | grep -E '^openjdk(@[0-9]+)?$' | tr '\n' ' ')"
  [ -n "$brew_jdks" ] && echo "  Homebrew JDKs: $brew_jdks"
fi
if [ -f package.json ] && command -v node >/dev/null 2>&1; then
  echo "  node: $(node -v)"
fi
if [ -f pyproject.toml ]; then
  command -v python3 >/dev/null 2>&1 && echo "  python3: $(python3 -V 2>&1)"
  command -v uv >/dev/null 2>&1 && echo "  uv: $(uv --version 2>&1)"
fi
if [ -f pubspec.yaml ]; then
  command -v fvm >/dev/null 2>&1 && echo "  fvm: present (run Flutter as 'fvm flutter')"
fi
