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

def test_text_integrity_dcc():
    response = client.get("oracle/Latin/result/dcc_latin_core_list/start/end/10/dcc_core_list/start-end")
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

def test_text_integrity_in_cat():
    response = client.get("oracle/Latin/result/cicero_in_catilinam_1-4/start/end/10/cicero_in_catilinam_1-4/1.1.1-1.1.2")
    assert response.status_code == 200


def test_stress():
    """Will 'fail' by killing the process"""
    response = client.get('/select/Latin/result/cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4+cicero_in_catilinam_1-4/start+start+start+start+start+start+start+start+start-end+end+end+end+end+end+end+end+end/running/')
    assert response.status_code == 200
    assert response.template.name == 'result.html'
    assert "request" in response.context
