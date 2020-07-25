Run App
==============

manual of running app (TMP)

-------


## local (`pipenv`)

activate pipenv-environment:

```
pipenv shell
```

run `app.main`

```
uvicorn app.main:app --reload
```
or using ssl:

```
uvicorn app.main:app --reload --ssl-keyfile=.ssl/server.key --ssl-certfile=.ssl/server.crt
```


## local (`conda`)

activate conda-environment:

```
conda activate fastapi_sqlalchemy
```

run `app.main`

```
uvicorn app.main:app --reload
```


## `docker-compose`

(...under construction...)

-----

## DB Migration

### local `sqlite3`

(...under construction...)

