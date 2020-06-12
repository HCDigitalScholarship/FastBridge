import importlib
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_select_latin():
    response = client.get("select/Latin")
    assert response.status_code == 200
    assert response.context["book_name"] == importlib.import_module('Latin').texts

def test_result_OvidPresent():
    response = client.get("/select/result/ovid_metamorphoses/1.1-1.1/")
    assert response.status_code == 200


def test_result_Ovid_start_and_end():
    response = client.get("/select/result/ovid_metamorphoses/1.1-1.781/")
    assert response.status_code == 200
    #should only fail with list index out of range
