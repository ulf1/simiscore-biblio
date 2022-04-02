from test.data import one_line_metadata

import pytest
from starlette.testclient import TestClient

from app.main import app, srvurl


@pytest.fixture
def test_online_metadata():
    return one_line_metadata


def test_read_info():
    client = TestClient(app)
    response = client.get(f"{srvurl}/")
    assert response.status_code == 200
    assert response.json() == {
        "version": "0.1.0",
        "metadata_scorer": [
            "max_k: 5",
            "multiline: False",
            "start_tag: fundstelle",
        ],
    }


def test_docs_reachable():
    client = TestClient(app)
    response = client.get(f"{srvurl}/docs")
    assert response.status_code == 200


def test_post_empty_list():
    client = TestClient(app)
    response = client.post(f"{srvurl}/similarities/", json=[])
    assert response.status_code == 200
    assert response.json() == {"ids": [], "matrix": []}


def test_post_request_one_line_strings(test_online_metadata):
    client = TestClient(app)
    response = client.post(
        f"{srvurl}/similarities/", json=test_online_metadata
    )
    result = [
        response.json()["matrix"][i][i]
        for i in range(len(test_online_metadata))
    ]
    assert response.status_code == 200
    assert pytest.approx(sum(result)) == len(test_online_metadata)
