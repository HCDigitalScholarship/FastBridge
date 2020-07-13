"""How to use:
Every function defined here must begin with test_
then type pytest in the shell
tests should end with an assert statment
"""
import importlib
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_text_integrity_oxford():
    response = client.get("oracle/Latin/result/oxford_latin_course_college/start/end/10/dcc_core_list/start-end")
    assert response.status_code == 200

def test_text_integrity_dcc():
    response = client.get("oracle/Latin/result/dcc_core_list/start/end/10/dcc_core_list/start-end")
    assert response.status_code == 200

def test_text_integrity_wheelock():
    response = client.get("oracle/Latin/result/wheelock_textbook/start/end/10/dcc_core_list/start-end")
    assert response.status_code == 200

def test_select_latin():
    response = client.get("select/Latin")
    assert response.status_code == 200
    assert response.context["book_name"] == importlib.import_module('Latin').texts

def test_select_greek():
    response = client.get("select/Greek")
    assert response.status_code == 200
    assert response.context["book_name"] == importlib.import_module('Greek').texts


def test_result_OvidPresent():
    response = client.post("/select/Latin/result/ovid_metamorphoses/1.1-1.1/running/")
    assert response.status_code == 200


def test_text_integrity_ovid12():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/1.1/2.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test
def test_text_integrity_ovid23():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/2.1/3.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test
def test_text_integrity_ovid34():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/3.1/4.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test

def test_text_integrity_ovid45():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/4.1/5.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test

def test_text_integrity_ovid56():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/5.1/6.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test

def test_text_integrity_ovid67():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/6.1/7.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test

def test_text_integrity_ovid78():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/7.1/8.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test



def test_text_integrity_ovid89():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/8.1/9.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test


def test_text_integrity_ovid910():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/9.1/10.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test


def test_text_integrity_ovid1011():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/10.1/11.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test


def test_text_integrity_ovid112():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/11.1/12.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test


def test_text_integrity_ovid1213():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/12.1/13.1/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test

def test_text_integrity_ovid13end():
    response = client.get("oracle/Latin/result/ovid_metamorphoses/13.1/end/10/dcc_core_list/start-end")
    assert response.status_code == 200
    #since oracle goes through pretty much every subsection of the text, if part of the text breaks, it will fail the test
