#!/bin/bash

# DB migration 실행하기
poetry run python -m api.migrate_cloud_db

# uvicorn의 서버를 실행한다.
poetry run uvicorn api.main:app --host 0.0.0.0