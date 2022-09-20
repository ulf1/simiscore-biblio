[![Join the chat at https://gitter.im/satzbeleg/community](https://badges.gitter.im/satzbeleg/community.svg)](https://gitter.im/satzbeleg/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


# simiscore-biblio
An ML API to compute similarity scores between meta information about sentence examples. 
The API is programmed with the [`fastapi` Python package](https://fastapi.tiangolo.com/), 
uses the packages [`datasketch`](http://ekzhu.com/datasketch/index.html) and [`kshingle`](https://github.com/ulf1/kshingle) to compute similarity scores.
The deployment is configured for Docker Compose.

## Docker Deployment
Call Docker Compose

```sh
export API_PORT=8081
docker-compose -f docker-compose.yml up --build
# or as oneliner:

API_PORT=8081 docker-compose up
```

(Start docker daemon before, e.g. `open /Applications/Docker.app` on MacOS).

Check

```sh
curl http://localhost:8081
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
# uvicorn app.main:app --reload
gunicorn app.main:app --reload --bind=0.0.0.0:8081 \
    --worker-class=uvicorn.workers.UvicornH11Worker \
    --workers=1 --timeout=600
```

### Run some requests

```sh
curl -X POST "http://localhost:8081/similarities/" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d '["Die Kuh macht muh.", "Die Muh macht kuh."]'
```

### Other commands and help
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`
- Show the docs: [http://localhost:8081/docs](http://localhost:8081/docs)
- Show Redoc: [http://localhost:8081/redoc](http://localhost:8081/redoc)


### Clean up 
```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


## Appendix

### Citation

### References
- Sebastián Ramírez, 2018, FastAPI, [https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)
- Eric Zhu, Vadim Markovtsev, aastafiev, Wojciech Łukasiewicz, ae-foster, Sinusoidal36, Ekevoo, Kevin Mann, Keyur Joshi, Peter Kubov, Qin TianHuan, Spandan Thakur, Stefano Ortolani, Titusz, Vojtech Letal, Zac Bentley, fpug, & oisincar. (2021). ekzhu/datasketch: v1.5.4 (v1.5.4). Zenodo. [https://doi.org/10.5281/zenodo.5758425](https://doi.org/10.5281/zenodo.5758425)
- Ulf Hamster. (2022). kshingle: Shingling text data (0.10.0). Zenodo. [https://doi.org/10.5281/zenodo.7096407](https://doi.org/10.5281/zenodo.7096407)
- Leonard Richardson, 2007, Beautiful soup, [https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/)

### Support
Please [open an issue](https://github.com/satzbeleg/simiscore-biblio/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/satzbeleg/simiscore-biblio/compare/).
