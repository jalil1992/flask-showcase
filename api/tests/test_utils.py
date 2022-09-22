from api.CALCutils.urls import API_UTILS_GET_AGE
from api.urls import API_UTILS
from CALCcomp.utils import get_age


def test_get_age(client):
    test_dob = "1989-05-05T00:00"
    response = client.post(API_UTILS + API_UTILS_GET_AGE, json={"date_of_birth": test_dob})
    assert response.status_code == 200
    assert response.get_json()["age"] == get_age(test_dob)
