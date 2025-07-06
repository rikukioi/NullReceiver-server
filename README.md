## Памятка по старту сервера

1. Загляни в папку src/certs и выполни указанные в том README команды.

2. Примени миграции Alembic. Для этого зайди в shell докер-контейнера сервера и выполни команды:
```shell
uv run alembic revision --autogenerate -m "init"
uv run alembic upgrade head
```
3. Сервер готов к использованию http://localhost:23156/docs