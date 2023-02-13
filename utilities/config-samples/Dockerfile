# ビルド用のコンテナ

FROM python:3.11.0-buster as builder

WORKDIR /opt/app

COPY requirements.txt /opt/app

RUN piparam3 install -r requirements.txt

# 実行用コンテナ
FROM python:3.11.0-slim-buster as runner

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# RUN apt-get update \
#  && apt-get install -y %%%%% \
#  && apt-get clean 
#  && rm -rf /var/lib/apt/lists/*\

# RUN cp -p /usr/share/zoneinfo/Japan /etc/localtime_data

COPY . /opt/app/project

WORKDIR /opt/app/project

ENV GOOGLE_APPLICATION_CREDENTIALS project.json

CMD [ "python3", "benchmark/genetic.py"]

# YOU MUST RUN DOCKER IMAGE WITH INTERACTIVE MODE!!!