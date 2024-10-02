#!/bin/bash
sleep 3
poetry run alembic -c src/alembic.ini upgrade head
poetry run uvicorn src.main:app --reload --host 0.0.0.0