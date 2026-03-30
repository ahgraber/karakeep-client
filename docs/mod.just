set quiet := true
set shell := ['bash', '-euo', 'pipefail', '-c']
set dotenv-load := true

root_dir := shell('git -C "' + justfile_directory() + '" rev-parse --show-toplevel')

[private]
default:
  @just --list docs --unsorted

[doc('Build docs, package zip, upload to Docat, and tag as latest.')]
publish: build upload tag

[doc('Build MkDocs site and package into a zip artifact.')]
build:
  cd "{{root_dir}}" && uv run --group docs mkdocs build
  mkdir -p "{{root_dir}}/docs-dist"
  rm -f "{{root_dir}}/docs-dist/karakeep-client-docs.zip"
  cd "{{root_dir}}/site" && zip -qr ../docs-dist/karakeep-client-docs.zip .

[doc('Resolve the docs version from git tag or pyproject.toml.')]
version:
  #!/usr/bin/env bash
  cd "{{root_dir}}"
  if git describe --tags --exact-match >/dev/null 2>&1; then
    git describe --tags --exact-match | sed 's/^v//'
  else
    uv run python -c 'import tomllib; from pathlib import Path; print(tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"])'
  fi

[doc('Upload docs zip to Docat. Requires DOCAT_HOST, DOCAT_PROJECT, DOCAT_TOKEN in .env.')]
upload: build
  #!/usr/bin/env bash
  cd "{{root_dir}}"
  version="$(just docs version)"
  curl -fsS -X POST \
    -H "Docat-Api-Key: ${DOCAT_TOKEN}" \
    -F "file=@docs-dist/karakeep-client-docs.zip" \
    "${DOCAT_HOST}/api/${DOCAT_PROJECT}/${version}"

[doc('Tag the current docs version as latest on Docat.')]
tag:
  #!/usr/bin/env bash
  cd "{{root_dir}}"
  version="$(just docs version)"
  curl -fsS -X PUT \
    -H "Docat-Api-Key: ${DOCAT_TOKEN}" \
    "${DOCAT_HOST}/api/${DOCAT_PROJECT}/${version}/tags/latest"
