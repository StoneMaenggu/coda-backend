## FastAPI를 통한 백엔드 서버 구축
Docker를 이용해 구축 후 AWS로 배포.

## 로컬에서 API 명세서 확인하는 법
1. 본 레포지토리를 clone
2. 도커 실행
3. 터미널에서 파일이 위치한 디렉토리로 이동하여 아래 코드 실행

```
docker compose build
docker compose run --entrypoint "poetry install --no-root" coda-app
docker compose build --no-cache
docker compose up

docker compose exec coda-app poetry run python -m api.migrate_db
docker compose exec db mysql codadb
```

4. http://localhost:8000/docs or http://localhost:8000/redoc 접속

## 디렉토리 구조
```bash
├── Dockerfile
├── Dockerfile.cloud
├── api
│   ├── __init__.py
│   ├── access.py
│   ├── cruds
│   │   ├── __init__.py
│   │   ├── group.py
│   │   ├── image.py
│   │   ├── login.py
│   │   ├── post.py
│   │   ├── reaction.py
│   │   └── user.py
│   ├── db.py
│   ├── main.py
│   ├── migrate_cloud_db.py
│   ├── migrate_db.py
│   ├── models
│   │   ├── __init__.py
│   │   └── tables.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── group.py
│   │   ├── image.py
│   │   ├── login.py
│   │   ├── post.py
│   │   ├── reaction.py
│   │   └── user.py
│   └── schemas
│       ├── __init__.py
│       ├── group.py
│       ├── image.py
│       ├── login.py
│       ├── post.py
│       ├── reaction.py
│       └── user.py
├── docker-compose.yaml
├── entrypoint.sh
├── poetry.lock
└── pyproject.toml
```

