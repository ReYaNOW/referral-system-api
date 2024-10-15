[![Linter check](1https://github.com/ReYaNOW/avito-tech-test-task/actions/workflows/pyci.yml/badge.svg)](https://github.com/ReYaNOW/avito-tech-test-task/actions/workflows/pyci.yml)

# RESTful API для реферальной системы

## Функционал
- Регистрация и аутентификация пользователя (JWT, Oauth 2.0).


- Аутентифицированный пользователь имеет возможность создать или удалить свой реферальный код.


- Одновременно может быть активен только 1 код. При создании кода обязательно должен быть задан его срок годности.


- Возможность регистрации по реферальному коду в качестве реферала.


- Получение информации о рефералах по id реферера.


## Особенности
- Реализована возможность запуска в Docker.
- Реализована валидация входных данных.
- UI документация Swagger
- Использование emailhunter.co для проверки указанного email адреса
- Кеширование реферальных кодов с использованием Redis

Стек: Python3.11, PostgreSQL, FastApi,
SqlAlchemy, Alembic, Asyncpg, Redis, Docker.

## Документация
Открыть Swagger документацию можно по [ссылке111111111111111111111](https://test-task-avito-tech.onrender.com/docs)
Там же можно поделать запросы к API

# Использование

 - Открыть задеплоенный [тестовый варasdasdasdadsasdasdиант](1https://avito-tech-test-task.onrender.com)
 - [Развернуть весь сервис в Docker](#Как-развернуть-весь-сервис-в-Docker)
 - [Развернуть сервис с Redis и PostgreSQL в Docker (для разработки)](#как-развернуть-сервис-с-redis-и-postgresql-в-docker-для-разработки)

![App preview](https://github.com/ReYaNOW/ReYaNOW/blob/main/Images/referral_preview.png?raw=true)

## Как развернуть весь сервис в Docker
1. Склонировать репозиторий

```
git clone https://github.com/ReYaNOW/referral-system-api.git
```

2. Переименовать .env.example в .env .
   [Опционально] Указать HUNTERIO_API_KEY для использования
валидации email (его можно найти [тут](https://hunter.io/api-keys))

```
mv .env.example .env
```

3. Создать, запустить контейнеры и применить миграции к БД

```
docker compose --profile full up --remove-orphans
```

4. Открыть http://127.0.0.1:8000/docs


<hr>

## Как развернуть сервис с Redis и PostgreSQL в Docker (для разработки)
Для этого необходим [Poetry](https://python-poetry.org/docs/#installing-with-pipx)

1. Склонировать репозиторий

```
git clone https://github.com/ReYaNOW/referral-system-api.git
```

2. Установить Python зависимости и pre-commit хуки

```
make install
```

3. Переименовать .env.example в .env .
   [Опционально] указать другие database url и redis_url для использования уже работающих БД.

   [Опционально] Указать HUNTERIO_API_KEY для использования
валидации email (его можно найти [тут](https://hunter.io/api-keys))

```
mv .env.example .env
```

4. Запустить PostgreSQL и Redis базы данных, если не указали свои url для них

```
docker compose up -d --remove-orphans
```

5. Запустить сервер и открыть http://127.0.0.1:8080/docs

```
make dev
```
