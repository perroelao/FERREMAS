import requests
import base64

CLIENT_ID = "ASrT5J3EI_5Z3bAcGWkfN7QfBB8n5yIUg-6NgNxudxWQ86EYeITctTxj1FaTKa30FVe2FbL1fqXVFa-8"
CLIENT_SECRET = "EN1Gb5w7b-ivM_ISxg7TIWL-AZnSf1MvQZyB2O1tImD5zzO0AsUnJqDXXfmLNyEfFpbgSl8OaTf7ym_k"

def get_paypal_access_token():
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        headers=headers,
        data=data
    )
    response.raise_for_status()
    return response.json()["access_token"]

def crear_orden_paypal(total):
    access_token = get_paypal_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    body = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": f"{float(total):.2f}"
            }
        }],
        "application_context": {
            "return_url": "http://localhost:8000/pago_exitoso/",
            "cancel_url": "http://localhost:8000/"
        }
    }
    response = requests.post(
        "https://api-m.sandbox.paypal.com/v2/checkout/orders",
        headers=headers,
        json=body
    )
    response.raise_for_status()
    data = response.json()
    approval_url = next(link["href"] for link in data["links"] if link["rel"] == "approve")
    return {"orderId": data["id"], "approvalUrl": approval_url}

def capturar_pago_paypal(order_id):
    access_token = get_paypal_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(
        f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture",
        headers=headers
    )
    response.raise_for_status()
    return response.json()