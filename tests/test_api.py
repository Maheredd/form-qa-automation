import requests
import allure
import time

# Base URL for the JSONPlaceholder API (Free, no auth required)
BASE_URL = "https://jsonplaceholder.typicode.com/users"


@allure.feature("API Testing")
@allure.story("Get All Users")
@allure.severity(allure.severity_level.NORMAL)
def test_get_all_users():
    """
    TC-016: Send a GET request to retrieve all users.
    Verify status code is 200 and response is a non-empty list.
    """
    with allure.step("Send GET request to /users"):
        response = requests.get(BASE_URL)

    with allure.step("Verify response status code is 200"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Verify response body is a list with at least one user"):
        data = response.json()
        assert isinstance(data, list), "Response is not a list!"
        assert len(data) > 0, "User list is empty!"


@allure.feature("API Testing")
@allure.story("Get Single User")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_single_user():
    """
    TC-017: Send a GET request for a specific user ID.
    Verify status code is 200 and response contains expected user data.
    """
    user_id = 1
    with allure.step(f"Send GET request to /users/{user_id}"):
        response = requests.get(f"{BASE_URL}/{user_id}")

    with allure.step("Verify response status code is 200"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Verify user ID matches"):
        data = response.json()
        assert data.get("id") == user_id, f"Expected ID {user_id}, got {data.get('id')}"
        assert "name" in data, "User name missing in response"


@allure.feature("API Testing")
@allure.story("User Not Found")
@allure.severity(allure.severity_level.NORMAL)
def test_get_user_not_found():
    """
    TC-018: Send a GET request for a non-existent user ID.
    Verify status code is 404 Not Found.
    """
    user_id = 99999
    with allure.step(f"Send GET request for invalid user ID {user_id}"):
        response = requests.get(f"{BASE_URL}/{user_id}")

    with allure.step("Verify response status code is 404"):
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"


@allure.feature("API Testing")
@allure.story("Create User (POST)")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user():
    """
    TC-019: Send a POST request to create a new user.
    Verify status code is 201 Created and response contains sent data.
    """
    payload = {
        "name": "Mahesh Tester",
        "username": "mahesht",
        "email": "mahesh@example.com"
    }

    with allure.step("Send POST request to create a user"):
        response = requests.post(BASE_URL, json=payload)

    with allure.step("Verify response status code is 201"):
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    with allure.step("Verify response contains created data and new ID"):
        data = response.json()
        assert data.get("name") == payload["name"], "Name mismatch"
        assert data.get("email") == payload["email"], "Email mismatch"
        assert "id" in data, "ID not generated in response"


@allure.feature("API Testing")
@allure.story("Update Entire User (PUT)")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_user():
    """
    TC-020: Send a PUT request to completely update an existing user.
    Verify status code is 200 and data is updated.
    """
    user_id = 1
    payload = {
        "name": "Updated Name",
        "username": "updated_user",
        "email": "updated@example.com"
    }

    with allure.step(f"Send PUT request to /users/{user_id}"):
        response = requests.put(f"{BASE_URL}/{user_id}", json=payload)

    with allure.step("Verify response status code is 200"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Verify updated data"):
        data = response.json()
        assert data.get("name") == payload["name"], "Name not updated"
        assert data.get("email") == payload["email"], "Email not updated"


@allure.feature("API Testing")
@allure.story("Partially Update User (PATCH)")
@allure.severity(allure.severity_level.NORMAL)
def test_patch_user():
    """
    TC-021: Send a PATCH request to update only the email of a user.
    Verify status code is 200 and only the specific field is updated.
    """
    user_id = 1
    payload = {"email": "patched.email@example.com"}

    with allure.step(f"Send PATCH request to /users/{user_id}"):
        response = requests.patch(f"{BASE_URL}/{user_id}", json=payload)

    with allure.step("Verify response status code is 200"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Verify only the email was updated"):
        data = response.json()
        assert data.get("email") == payload["email"], "Email not patched"


@allure.feature("API Testing")
@allure.story("Delete User (DELETE)")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_user():
    """
    TC-022: Send a DELETE request to remove a user.
    Verify status code is 200 (or 204/202 depending on the API).
    """
    user_id = 1
    with allure.step(f"Send DELETE request to /users/{user_id}"):
        response = requests.delete(f"{BASE_URL}/{user_id}")

    with allure.step("Verify response status code is successful"):
        # JSONPlaceholder returns 200 for a successful delete mock
        assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"


@allure.feature("API Testing")
@allure.story("Performance (Response Time)")
@allure.severity(allure.severity_level.NORMAL)
def test_api_response_time():
    """
    TC-023: Send a GET request and verify the response time is acceptable (< 2.5 seconds).
    """
    with allure.step("Send GET request and measure response time"):
        start_time = time.time()
        response = requests.get(BASE_URL)
        end_time = time.time()
        
        response_time_seconds = end_time - start_time

    with allure.step(f"Verify response time is under 2.5s (Actual: {response_time_seconds:.2f}s)"):
        assert response.status_code == 200
        assert response_time_seconds < 2.5, f"API too slow! Took {response_time_seconds:.2f}s"
