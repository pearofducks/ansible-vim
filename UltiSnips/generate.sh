#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

cd "$(dirname "$0")"

ANSIBLE_MODULE_LOCATION="$(ansible --version | grep "ansible python module location" | sed -E 's/ +ansible python module location += +//g')"
PYTHONPATH="$(dirname "$ANSIBLE_MODULE_LOCATION")"
PYTHON_VERSION=$(basename "$(dirname "$PYTHONPATH")")

export PYTHONPATH
exec "$PYTHON_VERSION" generate.py $@
