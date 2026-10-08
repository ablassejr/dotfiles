# Utility setup for linear-ticket-implementation

This package includes its own dependency manifest and installation scripts. Copying this skill does not require another skill directory for utility setup. The scripts support this user’s macOS environment; linked official sources cover other platforms.

## Select and check

Run from this skill’s directory, or use an absolute script path. The default checks only required utilities. Select optional utilities only when the task needs them. A successful check establishes utility availability, not authentication, a running service, or workflow completion.

```sh
bash scripts/setup.sh --check
bash scripts/setup.sh --plan --tool specflow
bash scripts/setup.sh --install --tool specflow
```

Repeat --tool to select several utilities. --plan prints the exact commands without running them. --check returns 0 when selected utilities are available and 2 when any is missing; argument or installation failures return 1. --install installs missing selected utilities and verifies their availability. It does not reinstall an adequate existing command. Read current documentation for the selected commands before execution and remain within the user’s installation authorization.

## Dependency purpose

| Utility | When needed | Purpose | Documentation |
| --- | --- | --- | --- |
| specflow | Only when selected | Packaged planning, content, visual, and workflow validation client | [Installation source](setup.md#bundled-specflow) |
| python | Only when selected | Run bundled Python helpers | [Installation source](https://formulae.brew.sh/formula/python) |
| c8ctl | Only when selected | Camunda linting, FEEL, templates, and selected cluster operations | [Installation source](https://www.npmjs.com/package/@camunda8/cli) |
| java | Only when selected | Java workers, connectors, tests, or local Camunda runtime | [Installation source](https://formulae.brew.sh/formula/openjdk@21) |
| node | Only when selected | Run Node utilities and npm packages | [Installation source](https://formulae.brew.sh/formula/node) |
| cloc | Only when selected | Measure maintained code | [Installation source](https://formulae.brew.sh/formula/cloc) |
| git | Only when selected | Read local source history and comparisons | [Installation source](https://formulae.brew.sh/formula/git) |
| archify | Only when selected | Render diagrams using the runtime bundled in this skill | [Installation source](https://github.com/tt-a1i/archify) |
| likec4 | Only when selected | Render formal architecture diagrams | [Installation source](https://www.npmjs.com/package/likec4) |

## Installation and activation

Python 3 runs the setup helper. If Python is missing, --install provisions it with Homebrew. If Homebrew is absent, the bundled bootstrap installs it through its official installer:

```sh
bash scripts/bootstrap.sh --install-homebrew
```

Homebrew may require macOS administrator access during bootstrap or a desktop application installation. The bootstrap does not edit shell startup files itself; upstream installation behavior is described by [Homebrew](https://docs.brew.sh/Installation). If system installation is unavailable, use an existing compatible runtime and the documented package-specific method.

Npm packages and Python libraries go into ~/.local/share/agent-skill-tools/linear-ticket-implementation by default. --prefix selects another directory; use the same prefix for installation, checking, and activation. Python libraries use a private virtual environment. Homebrew tools use Homebrew’s installation locations. No repository manifest, global Python environment, or agent credential settings are edited.

After a successful check or install, activate the selected environment in the current shell:

```sh
eval "$(bash scripts/setup.sh --check --env --tool specflow)"
```

This prints shell-quoted PATH, NODE_PATH, and Playwright browser-cache exports; when Java 21 is selected it also exposes its JAVA_HOME. Activation does not persist in shell startup files. The JSON result reports the prefix, selected utility locations, installation plan, and remaining external requirements. Use the prefix’s virtual-environment Python for helpers needing installed Python libraries, and its node_modules assets for media. Bundle replay/player assets with a shared document so readers do not depend on the author’s installation.

Use the selected project’s own dependency manifest and lockfile for application dependencies. The isolated toolkit supplies skill utilities and experiments; it does not claim that installing an SDK into this prefix adds it to the application’s build.

## Bundled specflow

Use scripts/specflow from this package, including when only one skill directory is copied. The runtime, schemas, and process definitions are bundled. Its local validators need Python; engine operations additionally require the selected live Camunda endpoint and authorization. Installing a CLI does not deploy a process or grant a human approval.

## Service and account requirements

- Agent connectors, authenticated accounts, provider permissions, and project configuration use the existing session. Package installation does not authenticate or grant write authority.

## Optional Camunda engine installation

For a selected local c8run deployment, use the bundled installer with the version required by the project, for example bash scripts/install-camunda-runtime.sh 8.8. It provisions c8ctl and Java if needed, then downloads that engine version through the documented c8ctl cluster install command. It does not start a cluster, configure credentials, or deploy workflow definitions. Existing remote clusters need no local engine installation. Choose and verify the compatible version before running this script.

## Bundled Archify

Select archify in setup, then use scripts/archify for the packaged renderer. Its [authoring guide](../vendor/archify/SKILL.md), schemas, examples, renderers, and assets are included in this skill; no neighboring Archify installation is required. For example, python3 scripts/archify validate architecture diagram.json --quality showcase --json.
