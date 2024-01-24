using poetry

poetry create python-shiny-neon

poetry add shiny

poetry shell for the virtual environment

shiny create

Starlette is a lightweight ASGI framework/toolkit, which is ideal for building async web services in Python.

```
(python-shiny-neon-ai-py3.12) 🐶 ➜  python-shiny-neon-ai shiny create
? Which template would you like to use?: Basic App
? Would you like to use Shiny Express? No
? Enter destination directory: ./
Created Shiny app at basic-app
Next steps open and edit the app file: basic-app/app.py
```

add in .gitignore

then init git

```
git init
```

add `.env`

and `config.py`

Add the export command if needed

https://github.com/python-poetry/poetry-plugin-export

pipx inject poetry poetry-plugin-export

poetry export --without-hashes --format=requirements.txt > requirements.txt

Using docker from here - https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/tree/master
