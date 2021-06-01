[![Total alerts](https://img.shields.io/lgtm/alerts/g/myorg/template-fastapi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/myorg/template-fastapi/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/myorg/template-fastapi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/myorg/template-fastapi/context:python)
[![template-fastapi](https://snyk.io/advisor/python/template-fastapi/badge.svg)](https://snyk.io/advisor/python/template-fastapi)


# TEMPLATE FASTAPI


## Docker Deployment
Call Docker Compose

```sh
export NUM_WORKERS=2
export API_PORT=12345
docker-compose up
# or as oneliner:
# NUM_WORKERS=2 API_PORT=12345 docker-compose up
```

(Start docker daemon before, e.g. `open /Applications/Docker.app` on MacOS).

Check

```sh
curl http://localhost:12345
curl "http://127.0.0.1:12345/items/5?q=somequery"
```

Notes: Only `main.py` is used in `Dockerfile`.



## Local Development

### Install a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)


### Start Server

```sh
source .venv/bin/activate
#uvicorn app.main:app --reload
gunicorn app.main:app --reload --bind=0.0.0.0:80 \
    --worker-class=uvicorn.workers.UvicornH11Worker --workers=2
```

Notes: 

- In the Dockerfile also the argument `--worker-tmp-dir=/dev/shm` is set what default path to a docker container's "in-memory filesystem", i.e. the temporary folder.
- The `uvicorn.workers.UvicornWorker` worker can use HTTPS certificates by adding the arguments `--keyfile=./key.pem --certfile=./cert.pem` (see [Setup HTTPS for uvicorn](https://www.uvicorn.org/deployment/#running-with-https))


### Run some requests

```sh
curl http://localhost:80
curl "http://localhost:80/items/5?q=somequery"
```

### Other commands and help
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`
- Show the docs: [http://localhost:80/docs`](http://localhost:80/docs`)
- Show Redoc: [http://localhost:80/redoc](http://localhost:80/redoc)


### Clean up 
```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


## Appendix

### Support
Please [open an issue](https://github.com/myorg/template-fastapi/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/myorg/template-fastapi/compare/).
