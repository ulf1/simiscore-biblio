[![DOI](https://zenodo.org/badge/355466087.svg)](https://zenodo.org/badge/latestdoi/355466087)


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

API_PORT=8081 docker-compose up --build
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
    -d '[
        "Christ, Lena: Die Rumplhanni. In: Deutsche Literatur von Frauen, Berlin: Directmedia Publ. 2001 [1917], S. 13229", 
        "Christ, Lena: Erinnerungen einer Überflüssigen. In: Deutsche Literatur von Frauen, Berlin: Directmedia Publ. 2001 [1912], S. 12498"
    ]'
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
```
@software{ulf_hamster_2022_7096467,
  author       = {Ulf Hamster and
                  Luise Köhler},
  title        = {simiscore-biblio: ML API for bibliographic similarities},
  month        = sep,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.7096467},
  url          = {https://doi.org/10.5281/zenodo.7096467}
}
```

### References
- Sebastián Ramírez, 2018, FastAPI, [https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)
- Eric Zhu, Vadim Markovtsev, aastafiev, Wojciech Łukasiewicz, ae-foster, Sinusoidal36, Ekevoo, Kevin Mann, Keyur Joshi, Peter Kubov, Qin TianHuan, Spandan Thakur, Stefano Ortolani, Titusz, Vojtech Letal, Zac Bentley, fpug, & oisincar. (2021). ekzhu/datasketch: v1.5.4 (v1.5.4). Zenodo. [https://doi.org/10.5281/zenodo.5758425](https://doi.org/10.5281/zenodo.5758425)
- Ulf Hamster. (2022). kshingle: Shingling text data (0.10.0). Zenodo. [https://doi.org/10.5281/zenodo.7096407](https://doi.org/10.5281/zenodo.7096407)
- Leonard Richardson, 2007, Beautiful soup, [https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/)

### Support
Please [open an issue](https://github.com/satzbeleg/simiscore-biblio/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/satzbeleg/simiscore-biblio/compare/).

### Acknowledgements
The "Evidence" project was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - [433249742](https://gepris.dfg.de/gepris/projekt/433249742) (GU 798/27-1; GE 1119/11-1).

### Maintenance
- till 31.Aug.2023 (v0.1.0) the code repository was maintained within the DFG project [433249742](https://gepris.dfg.de/gepris/projekt/433249742)
- since 01.Sep.2023 (v0.2.0) the code repository is maintained by Ulf Hamster.
