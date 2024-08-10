# python3.11 이미지 다운로드
FROM python:3.11-buster
# python의 출력 표시를 Docker에 맞게 조정한다.
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# pip를 사용하여 poetry를 설치한다.
RUN pip install "poetry==1.6.1"

# poetry의 정의 파일 복사 (존재하는 경우)
COPY pyproject.toml* poetry.lock* ./

# poetry로 라이브러리 설치 (pyproject.toml이 이미 존재하는 경우)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# uvicorn 서버 실행하기
ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]