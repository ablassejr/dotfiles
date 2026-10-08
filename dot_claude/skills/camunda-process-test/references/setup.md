# Utility setup for camunda-process-test

This package includes its own dependency manifest and installation scripts. Copying this skill does not require another skill directory for utility setup. The scripts support this user’s macOS environment; linked official sources cover other platforms.

## Select and check

Run from this skill’s directory, or use an absolute script path. The default checks only required utilities. Select optional utilities only when the task needs them. A successful check establishes utility availability, not authentication, a running service, or workflow completion.

```sh
bash scripts/setup.sh --check
bash scripts/setup.sh --plan --tool c8ctl
bash scripts/setup.sh --install --tool c8ctl
```

Repeat --tool to select several utilities. --plan prints the exact commands without running them. --check returns 0 when selected utilities are available and 2 when any is missing; argument or installation failures return 1. --install installs missing selected utilities and verifies their availability. It does not reinstall an adequate existing command. Read current documentation for the selected commands before execution and remain within the user’s installation authorization.

## Dependency purpose

| Utility | When needed | Purpose | Documentation |
| --- | --- | --- | --- |
| c8ctl | Only when selected | Camunda linting, FEEL, templates, and selected cluster operations | [Installation source](https://www.npmjs.com/package/@camunda8/cli) |
| dmnlint | Only when selected | Validate DMN structure | [Installation source](https://www.npmjs.com/package/dmnlint) |
| java | Required for this workflow | Java workers, connectors, tests, or local Camunda runtime | [Installation source](https://formulae.brew.sh/formula/openjdk@21) |
| maven | Required for this workflow | Build selected Java projects | [Installation source](https://formulae.brew.sh/formula/maven) |
| docker | Required for this workflow | Container-backed test or analysis workflow | [Installation source](https://formulae.brew.sh/cask/docker-desktop) |
| node | Only when selected | Run Node utilities and npm packages | [Installation source](https://formulae.brew.sh/formula/node) |

## Installation and activation

Python 3 runs the setup helper. If Python is missing, --install provisions it with Homebrew. If Homebrew is absent, the bundled bootstrap installs it through its official installer:

```sh
bash scripts/bootstrap.sh --install-homebrew
```

Homebrew may require macOS administrator access during bootstrap or a desktop application installation. The bootstrap does not edit shell startup files itself; upstream installation behavior is described by [Homebrew](https://docs.brew.sh/Installation). If system installation is unavailable, use an existing compatible runtime and the documented package-specific method.

Npm packages and Python libraries go into ~/.local/share/agent-skill-tools/camunda-process-test by default. --prefix selects another directory; use the same prefix for installation, checking, and activation. Python libraries use a private virtual environment. Homebrew tools use Homebrew’s installation locations. No repository manifest, global Python environment, or agent credential settings are edited.

After a successful check or install, activate the selected environment in the current shell:

```sh
eval "$(bash scripts/setup.sh --check --env)"
```

This prints shell-quoted PATH, NODE_PATH, and Playwright browser-cache exports; when Java 21 is selected it also exposes its JAVA_HOME. Activation does not persist in shell startup files. The JSON result reports the prefix, selected utility locations, installation plan, and remaining external requirements. Use the prefix’s virtual-environment Python for helpers needing installed Python libraries, and its node_modules assets for media. Bundle replay/player assets with a shared document so readers do not depend on the author’s installation.

Use the selected project’s own dependency manifest and lockfile for application dependencies. The isolated toolkit supplies skill utilities and experiments; it does not claim that installing an SDK into this prefix adds it to the application’s build.

## Service and account requirements

- A running compatible Camunda cluster and its chosen profile/credentials are needed only for engine operations. Local linting and drafting do not need a cluster.
- Agent connectors, authenticated accounts, provider permissions, and project configuration use the existing session. Package installation does not authenticate or grant write authority.
- Docker Desktop must be running for container workflows. Tool installation does not start the daemon or prepare project-specific images.

## Optional Camunda engine installation

For a selected local c8run deployment, use the bundled installer with the version required by the project, for example bash scripts/install-camunda-runtime.sh 8.8. It provisions c8ctl and Java if needed, then downloads that engine version through the documented c8ctl cluster install command. It does not start a cluster, configure credentials, or deploy workflow definitions. Existing remote clusters need no local engine installation. Choose and verify the compatible version before running this script.

# CPT test-harness setup

Prerequisites and one-time test-harness scaffold for `camunda-process-test-spring`.

## Prerequisites

- Java 21+
- Maven
- Docker runtime (required because CPT runs Zeebe in a Testcontainers container)

Use this skill’s bundled scripts/setup.sh to install selected java, maven, and docker utilities. The prerequisites below describe the test harness.

> Testcontainers pulls the matching Zeebe image automatically on first run (~500MB). Do not pre-pull `camunda/zeebe:latest` — the tag may not match the CPT version on the classpath.

## Readiness preflight (first run)

Run this quick check before scaffolding:

```bash
# Java runtime
java -version

# Maven (prefer wrapper when present)
./mvnw -version 2>/dev/null || mvn -version

# Docker runtime
docker info --format '{{.ServerVersion}}'
```

If Docker is not running, start your runtime (Docker Desktop, OrbStack, or Rancher Desktop) and re-run `docker info --format '{{.ServerVersion}}'`.

If Java or Maven resolves in an interactive shell but fails in non-interactive runs, check tool-manager shims (`asdf`/`mise`) and set the project toolchain explicitly (for example via `.tool-versions`) before running CPT.

## CPT dependency

Required entry in the project (or test harness) `pom.xml`:

```xml
<properties>
  <java.version>21</java.version>
  <camunda-process-test.version>8.9.0</camunda-process-test.version>
</properties>

<dependencies>
  <dependency>
    <groupId>io.camunda</groupId>
    <artifactId>camunda-process-test-spring</artifactId>
    <version>${camunda-process-test.version}</version>
    <scope>test</scope>
  </dependency>
  <dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
  </dependency>
</dependencies>
```

Use 8.9+ — the instruction-based `.test.json` format (`CREATE_PROCESS_INSTANCE`, `COMPLETE_JOB`, …) requires it.

### Spring Boot 4.x pin (CPT 8.9.x only)

CPT 8.9.x ships against Spring Boot 4.x. If the project already imports `spring-boot-dependencies` (e.g. via a parent BOM), pin the version explicitly or omit the BOM:

```xml
<properties>
  <spring-boot.version>4.0.5</spring-boot.version>
</properties>
```

The mismatch surfaces as `NoClassDefFoundError` on `AdditionalPathsMapper` or `HealthEndpointConfiguration` when the Spring `ApplicationContext` starts — it looks like a code problem but is purely a dependency-resolution issue. CPT 8.8.x ran against Spring Boot 3.x; do not carry a 3.x pin forward when upgrading.

## Scaffold layout

```
src/
  main/resources/
    processes/                        # BPMN, DMN, .form lives here
  test/
    java/io/camunda/tests/
      ProcessTest.java                # JUnit runner
      TestApplication.java            # @SpringBootApplication for tests
    resources/
      scenarios/
        <processId>.test.json         # one file per process
```

### `ProcessTest.java`

```java
package io.camunda.tests;

import io.camunda.process.test.api.CamundaSpringProcessTest;
import io.camunda.process.test.api.TestDeployment;
import io.camunda.process.test.api.testCases.TestCase;
import io.camunda.process.test.api.testCases.TestCaseRunner;
import io.camunda.process.test.api.testCases.TestCaseSource;
import org.junit.jupiter.params.ParameterizedTest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
@CamundaSpringProcessTest
@TestDeployment(resources = {
    "processes/expense-approval.bpmn",
    "processes/approval-routing.dmn",
    "processes/manager-review.form"
})
public class ProcessTest {

    @Autowired
    private TestCaseRunner testCaseRunner;

    @ParameterizedTest(name = "{0}")
    @TestCaseSource(directory = "/scenarios")
    void shouldPass(final TestCase testCase, final String fileName) {
        testCaseRunner.run(testCase);
    }
}
```

Notes:

- `@TestDeployment` paths are **classpath-relative**. Do **not** prefix with `classpath:` — CPT adds it internally; the prefix causes `FileNotFoundException`.
- Every BPMN, DMN, and form file referenced by the process under test must be listed. A missing `.form` produces a `FORM_NOT_FOUND` incident at runtime.
- `@TestCaseSource(directory = "/scenarios")` is classpath-relative — leading slash, regardless of the Java package.

### `TestApplication.java`

```java
package io.camunda.tests;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TestApplication {
    public static void main(String[] args) {
        SpringApplication.run(TestApplication.class, args);
    }
}
```

Required so `@SpringBootTest` has an application context to load.

## Node.js project layout

If the project root has `package.json` but no `pom.xml`, scaffold a sibling `test/` directory holding its own `pom.xml`. The test harness reads BPMN / DMN / form files from the parent project via a `<testResource>` mapping:

```xml
<testResources>
  <testResource>
    <directory>src/test/resources</directory>
    <excludes><exclude>scenarios/**</exclude></excludes>
  </testResource>
  <testResource>
    <directory>../resources</directory>
    <targetPath>processes</targetPath>
    <includes>
      <include>**/*.bpmn</include>
      <include>**/*.dmn</include>
      <include>**/*.form</include>
    </includes>
  </testResource>
</testResources>
```

Confirm the scaffold by running `mvn test-compile` from `test/`.

## Filename hygiene

Spaces in BPMN filenames work in Java strings and `<include>` tags but break shell scripts and glob patterns. Rename spaces to hyphens before adding to `@TestDeployment`.
