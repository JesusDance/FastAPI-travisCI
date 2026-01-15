def test_no_expenses_list(test_client, second_user_token):
    response = test_client.get(
        "/expenses",
        headers={"Authorization": f"Bearer {second_user_token}"}
    )
    json_response = response.json()

    assert response.status_code == 200
    assert json_response == []


def test_expenses_list(test_client, default_user_token):
    response = test_client.get(
        "/expenses",
        headers={"Authorization": f"Bearer {default_user_token}"}
    )
    json_response = response.json()

    assert response.status_code == 200
    assert json_response[0]["title"] == "some_title1"
    assert json_response[1]["title"] == "some_title2"
    assert json_response[2]["title"] == "some_title3"
    assert len(json_response) > 0


def test_full_expense_flow(test_client, default_user_token):
    created_expense_res = test_client.post(
        "/expenses",
        json={
            "title": "Expense",
            "amount": 100
        },
        headers={"Authorization": f"Bearer {default_user_token}"}
    )
    json_response = created_expense_res.json()

    assert created_expense_res.status_code == 201
    assert json_response["title"] == "Expense"
    assert json_response["amount"] == 100

    created_expense_id = json_response["id"]

    received_expense_res = test_client.get(
        f"/expenses/{created_expense_id}",
        headers={"Authorization": f"Bearer {default_user_token}"}
    )
    json_response = received_expense_res.json()

    assert received_expense_res.status_code == 200
    assert json_response["title"] == "Expense"

    received_expenses_res = test_client.get(
        "/expenses",
        headers={"Authorization": f"Bearer {default_user_token}"}
    )
    json_response = received_expenses_res.json()

    assert received_expenses_res.status_code == 200
    assert json_response[0]["title"] == "some_title1"

    updated_expense_res = test_client.patch(
        f"/expenses/{created_expense_id}",
        json={
            "title": "Updated_expense"
        },
        headers={"Authorization": f"Bearer {default_user_token}"}
    )
    json_response = updated_expense_res.json()

    assert updated_expense_res.status_code == 200
    assert json_response["title"] == "Updated_expense"

    deleted_expense_res = test_client.delete(
        f"/expenses/{created_expense_id}",
        headers={"Authorization": f"Bearer {default_user_token}"}
    )
    json_response = deleted_expense_res.json()

    assert deleted_expense_res.status_code == 200
    assert json_response["message"] == f"Expense {created_expense_id} deleted successfully"


