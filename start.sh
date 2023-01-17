#!/bin/sh

alembic upgrade head

python -m python_fastapi_stack
