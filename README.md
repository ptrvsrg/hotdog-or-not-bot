<h1 align="center">Hotdog or Not Bot</h1>

<p align="center">
  <img alt="License" src="https://img.shields.io/github/license/ptrvsrg/hotdog-or-not-bot?color=56BEB8&style=flat">
  <img alt="Github issues" src="https://img.shields.io/github/issues/ptrvsrg/hotdog-or-not-bot?color=56BEB8&style=flat" />
  <img alt="Github forks" src="https://img.shields.io/github/forks/ptrvsrg/hotdog-or-not-bot?color=56BEB8&style=flat" />
  <img alt="Github stars" src="https://img.shields.io/github/stars/ptrvsrg/hotdog-or-not-bot?color=56BEB8&style=flat" />
</p>

## About

Have you watched the HBO comedy series "Silicon Valley"? Have you remembered the Hotdog or Not app
that Jian Yang developed? This app identifies whether something is hotdog or not.

## Features

+ Detecting objects in the photo
+ Hotdog prediction
+ Telegram bot
+ Saving dataset to Yandex Disk

## Technologies

- [aiogram](https://aiogram.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [YOLO V8](https://www.ultralytics.com/yolo)
- [OpenCV](https://opencv.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [i18next](https://pypi.org/project/i18next/)
- [yadisk](https://yadisk.readthedocs.io/ru/latest/)

## Requirements

Before starting, you need to have:

+ [Git](https://git-scm.com)
+ [Python](https://www.python.org/)
+ [Docker](https://www.docker.com/)
+ [ngrok](https://ngrok.com/)

## Starting

### Local

1. Clone this project

```shell
git clone https://github.com/ptrvsrg/hotdog-or-not-bot.git
cd hotdog-or-not-bot
```

2. Create virtual environments

```shell
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```shell
pip install -r requirements.txt
```

4. (Optional) Run http tunnel

> **_NOTE:_** Run in a separate terminal.

> **_NOTE:_** ngrok is a globally distributed reverse proxy. We will use it to test the webhook.
> After launching we have to copy forwarding URL.

```shell
ngrok http 8080
```

5. Set up environment variables

> **_NOTE:_** Initialize environment variable **WEBHOOK_URL** with the value \<public URL\>/webhook

```shell
cp .env.local.exmaple .env
nano .env
export $(cat .env | xargs)
```

6. Start database and cache

```shell
docker compose --file docker-compose.local.yml --env-file .env up -d
```

7. Run application:

```shell
python app/main.py
```

### Docker

1. Install `docker-compose.yml`:

```shell
wget https://raw.githubusercontent.com/ptrvsrg/hotdog-or-not-bot/<release_version>/docker-compose.yml
```

2. Install example environment file:

```shell
wget https://raw.githubusercontent.com/ptrvsrg/hotdog-or-not-bot/<release_version>/.env.docker.example
```

3. Set up environment variables

> **_NOTE:_** Initialize environment variable **WEBHOOK_URL** with the value \<public URL\>/webhook

```shell
cp .env.docker.example .env
nano .env
```

4. Run containers:

```shell
docker compose --file docker-compose.yml --env-file .env up -d
```

## Contribution to the project

If you want to contribute to the project, you can follow these steps:

1. Create a fork of this repository.
2. Make the necessary changes.
3. Create a pull request describing your changes.
