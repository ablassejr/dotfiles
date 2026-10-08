# Utility setup for prisma-database-setup

This package includes its own dependency manifest and installation scripts. Copying this skill does not require another skill directory for utility setup. The scripts support this user’s macOS environment; linked official sources cover other platforms.

## Select and check

Run from this skill’s directory, or use an absolute script path. The default checks only required utilities. Select optional utilities only when the task needs them. A successful check establishes utility availability, not authentication, a running service, or workflow completion.

```sh
bash scripts/setup.sh --check
bash scripts/setup.sh --plan --tool prisma
bash scripts/setup.sh --install --tool prisma
```

Repeat --tool to select several utilities. --plan prints the exact commands without running them. --check returns 0 when selected utilities are available and 2 when any is missing; argument or installation failures return 1. --install installs missing selected utilities and verifies their availability. It does not reinstall an adequate existing command. Read current documentation for the selected commands before execution and remain within the user’s installation authorization.

## Dependency purpose

| Utility | When needed | Purpose | Documentation |
| --- | --- | --- | --- |
| prisma | Only when selected | Selected Prisma CLI workflow | [Installation source](https://www.npmjs.com/package/prisma) |
| prisma-client | Only when selected | Selected Prisma client workflow | [Installation source](https://www.npmjs.com/package/@prisma/client) |
| prisma-pg | Only when selected | Selected Postgres driver adapter | [Installation source](https://www.npmjs.com/package/@prisma/adapter-pg) |
| pg | Only when selected | Selected Postgres driver | [Installation source](https://www.npmjs.com/package/pg) |
| dotenv | Only when selected | Selected project environment loading | [Installation source](https://www.npmjs.com/package/dotenv) |
| node | Only when selected | Run Node utilities and npm packages | [Installation source](https://formulae.brew.sh/formula/node) |
| npm-prisma-adapter-mariadb | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/@prisma/adapter-mariadb) |
| npm-mariadb | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/mariadb) |
| npm-prisma-adapter-ppg | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/@prisma/adapter-ppg) |
| npm-prisma-ppg | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/@prisma/ppg) |
| npm-prisma-adapter-better-sqlite3 | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/@prisma/adapter-better-sqlite3) |
| npm-better-sqlite3 | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/better-sqlite3) |
| npm-prisma-adapter-libsql | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/@prisma/adapter-libsql) |
| npm-libsql-client | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/@libsql/client) |
| npm-prisma-adapter-mssql | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/@prisma/adapter-mssql) |
| npm-mssql | Only when selected | Selected package used by the skill’s executable examples; integrate application dependencies through their project manifest | [Installation source](https://www.npmjs.com/package/mssql) |

## Installation and activation

Python 3 runs the setup helper. If Python is missing, --install provisions it with Homebrew. If Homebrew is absent, the bundled bootstrap installs it through its official installer:

```sh
bash scripts/bootstrap.sh --install-homebrew
```

Homebrew may require macOS administrator access during bootstrap or a desktop application installation. The bootstrap does not edit shell startup files itself; upstream installation behavior is described by [Homebrew](https://docs.brew.sh/Installation). If system installation is unavailable, use an existing compatible runtime and the documented package-specific method.

Npm packages and Python libraries go into ~/.local/share/agent-skill-tools/prisma-database-setup by default. --prefix selects another directory; use the same prefix for installation, checking, and activation. Python libraries use a private virtual environment. Homebrew tools use Homebrew’s installation locations. No repository manifest, global Python environment, or agent credential settings are edited.

After a successful check or install, activate the selected environment in the current shell:

```sh
eval "$(bash scripts/setup.sh --check --env --tool prisma)"
```

This prints shell-quoted PATH, NODE_PATH, and Playwright browser-cache exports; when Java 21 is selected it also exposes its JAVA_HOME. Activation does not persist in shell startup files. The JSON result reports the prefix, selected utility locations, installation plan, and remaining external requirements. Use the prefix’s virtual-environment Python for helpers needing installed Python libraries, and its node_modules assets for media. Bundle replay/player assets with a shared document so readers do not depend on the author’s installation.

Use the selected project’s own dependency manifest and lockfile for application dependencies. The isolated toolkit supplies skill utilities and experiments; it does not claim that installing an SDK into this prefix adds it to the application’s build.
