# Utility setup for teach

This instruction-only skill declares no additional local utilities. Its bundled checker reports that empty selection. The application or repository being worked on supplies its own runtime and dependency manifest; use those declared dependencies when executing project commands. Native connectors are capabilities of the host session and are discovered there.

```sh
bash scripts/setup.sh --check
```

## Dependency purpose

No additional local utilities are declared.

## Installation and activation

The checker runs with Python 3. If Python is missing, --install provisions it through Homebrew. Run bash scripts/bootstrap.sh --install-homebrew when Homebrew is absent. --plan prints commands without installing; --tool selects a declared utility. This package does not install an agent host or configure authenticated connectors.
