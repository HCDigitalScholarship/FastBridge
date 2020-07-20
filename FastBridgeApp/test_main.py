"""How to use:
Every function defined here must begin with test_
then type pytest in the shell
tests should end with an assert statment
"""
import importlib
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
"""
def test_text_integrity_oxford():
    response = client.get("oracle/Latin/result/oxford_latin_course_college/start/end/10/dcc_core_list/start-end")
    assert response.status_code == 200



def test_text_integrity_wheelock():
    response = client.get("oracle/Latin/result/wheelock_textbook/start/end/10/dcc_core_list/start-end")
    assert response.status_code == 200"""

def test_select_latin():
    response = client.get("select/Latin")
    assert response.status_code == 200
    assert response.context["book_name"] == importlib.import_module('data.Latin.texts').texts

"""def test_select_greek():
    response = client.get("select/Greek")
    assert response.status_code == 200
    assert response.context["book_name"] == importlib.import_module('data.Greek.texts').texts
"""

def test_text_integrity_dcc():
    response = client.get("oracle/Latin/result/dcc_latin_core_list/start/end/10/cicero_in_catilinam_1-4/1.1.1-1.1.2")
    assert response.status_code == 200


def test_text_integrity_in_cat():
    response = client.get("oracle/Latin/result/cicero_in_catilinam_1-4/start/end/10/cicero_in_catilinam_1-4/1.1.1-1.1.2")
    assert response.status_code == 200


def test_text_integrity_testamentum_porcelli():
    response = client.get("oracle/Latin/result/testamentum_porcelli/start/end/1/cicero_in_catilinam_1-4/1.1.1-1.1.2")
    #note: this is a very, very small text with only 4 sections
    assert response.status_code == 200

def test_text_integrity_BG():
    response = client.get("oracle/Latin/result/caesar_bellum_gallicum/start/end/10/cicero_in_catilinam_1-4/1.1.1-1.1.2")
    assert response.status_code == 200

def test_text_whole_BG():
    response = client.get("/select/Latin/result/caesar_bellum_gallicum/start-end/running/")
    assert response.status_code == 200


#def test_text_integrity_de_rerum_nat():
#    response = client.get("oracle/Latin/result/lucretius_de_rerum_natura/start/end/10/cicero_in_catilinam_1-4/1.1.1-1.1.2")
#    assert response.status_code == 200




"""
def test_stress():
    #Will fail by killing the process
    response = client.get('/select/Latin/result/cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4/start+start+start+start+start+start+start+start+start-end+end+end+end+end+end+end+end+end/running/')
    assert response.status_code == 200
    assert response.template.name == 'result.html'
    assert "request" in response.context"""
