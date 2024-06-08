#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

uvicorn main:app --port 8080 --host 0.0.0.0
