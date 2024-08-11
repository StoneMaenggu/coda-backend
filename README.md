## FastAPI를 통한 백엔드 서버 구축
Docker를 이용해 구축 후 AWS로 배포할 예정.

## API 명세서 확인하는 법
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


여기서 작동하는대로 각자 DB에 작성되므로 post를 먼저 수행해야 에러가 안남!
아직 데이터 없을 때 오류나는 부분 raise 처리 다 안되어 있음!!
