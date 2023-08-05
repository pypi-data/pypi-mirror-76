#!/usr/bin/env bash

set -e
set -x

mypy wkstools/

flake8 wkstools/

black --check wkstools/ --diff

bandit -r wkstools/
