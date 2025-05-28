#OMG no way our first unit test file
from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

#format of tests
def test_stats_index():
    # Make a request to the "/stats/" endpoint and assert the response
    response = client.get("/stats/")
    assert response.status_code == 200
    #can add more assertions here 






'''
Formatting Tests:
# In stats.py
def add(a, b):
    return a + b

# In test_example.py
from FastBridgeApp.stats import add

def test_add():
    assert add(2, 3) == 5
    #THIS IS A TEST CASE
'''