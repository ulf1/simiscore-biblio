[![Join the chat at https://gitter.im/satzbeleg/community](https://badges.gitter.im/satzbeleg/community.svg)](https://gitter.im/satzbeleg/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/satzbeleg/simiscore-legal.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/simiscore-legal/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/satzbeleg/simiscore-legal.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/satzbeleg/simiscore-legal/context:python)



# simiscore-legal
An ML API to compute similarity scores between sentence examples based on their meta information. 
The API is programmed with the [`fastapi` Python package](https://fastapi.tiangolo.com/), 
uses the packages [`datasketch`](http://ekzhu.com/datasketch/index.html) and [`kshingle`](https://github.com/ulf1/kshingle) to compute similarity scores.
The deployment is configured for Docker Compose.

## Docker Deployment
Call Docker Compose

```sh
export API_PORT=12345
docker-compose -f docker-compose.yml up --build
# or as oneliner:

API_PORT=12345 docker-compose up
```

(Start docker daemon before, e.g. `open /Applications/Docker.app` on MacOS).


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
uvicorn app.main:app --reload
# gunicorn app.main:app --reload --bind=0.0.0.0:8080 \
#     --worker-class=uvicorn.workers.UvicornH11Worker --workers=2
```


### Other commands and help
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`
- Show the docs: [http://localhost:80/docs](http://localhost:80/docs)
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
Please [open an issue](https://github.com/satzbeleg/simiscore-legal/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/satzbeleg/simiscore-legal/compare/).
