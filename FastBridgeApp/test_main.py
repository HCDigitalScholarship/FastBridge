import importlib
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_select_latin():
    response = client.get("select/Latin")
    assert response.status_code == 200
    assert response.context["book_name"] == importlib.import_module('Latin').texts

def test_result_OvidPresent():
    response = client.post("/select/result/ovid_metamorphoses/1.1-1.1/running")
    assert response.status_code == 200


def verify_text_integrity_ovid():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/start/end/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test

def verify_text_integrity_oxford():
    response = client.get("oracle/Latin/result/oxford_latin_course_college/start/end/10/dcc_core_list/start-end")
    assert response.status_code == 200

def verify_text_integrity_dcc():
    response = client.get("oracle/Latin/result/dcc_core_list/start/end/10/dcc_core_list/start-end")
    assert response.status_code == 200

def verify_text_integrity_wheelock():
    response = client.get("oracle/Latin/result/wheelock_textbook/start/end/10/dcc_core_list/start-end")
    assert response.status_code == 200
