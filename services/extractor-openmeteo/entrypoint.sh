#!/bin/bash

set -e

python -m src.main || true

exec supercronic /app/crontab