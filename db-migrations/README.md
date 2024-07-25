# whatsapp-webhook-template-db-migrations

## Use case

This repository make migrations for postgresql

## Create migrations

To create new migrations file simply run command:  

```bash
alembic revision --autogenerate -m 'commit message'
```

## Run migrations

To run migrations, fill env in console

```bash
export POSTGRES_HOST=127.0.0.1
export POSTGRES_PORT=5432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=dbname
```

and run

```bash
python migrate.py
```
