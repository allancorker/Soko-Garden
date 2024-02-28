import requests # This module is a third party library used for making HTTP requests
import datetime # This module provides classes for working with dates and time
import base64 # This module provides functions to encode binary to ASCII characters using base 64 encoding and decode base 64 data back to its original binary form
from requests.auth import HTTPBasicAuth # Auth module contains authentication handlers for request

def stk_push(phone, amount):
    # GENERATING THE ACCESS TOKEN
    # create an account on safaricom daraja, here you are provided with below Credentials (Consumer Key and Secret Key)
    # For testing Purposes we use MODCOM Credentials
    consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
    consumer_secret = "amFbAoUByPV2rM5A"

    # Pass Consumer and Secret Key to Mpesa URL
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" # AUTH URL
    data = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)).json()

    # We get access token from data above - To be used Later
    access_token = data['access_token']

    # GETTING THE PASSWORD
    timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    business_short_code = "174379"
    # Combine the above 3 variables into single variable called "dats"
    data = business_short_code + passkey + timestamp
    # We encode data into base64(ASCII)
    encoded = base64.b64encode(data.encode())
    # Decode with utf-8
    # This might be useful if you need to pass this string as a parameter in an API request
    # Its a requirement by Safaricom to be in UTF-8(web)
    password = encoded.decode('utf-8')
    print(password)

    # BODY OR PAYLOAD
    payload = {
    "BusinessShortCode": "174379",
    "Password": "{}".format(password),
    "Timestamp": "{}".format(timestamp),
    "TransactionType": "CustomerPayBillOnline",
    "Amount": amount, # use 1 when testing
    "PartyA": phone, # change to your number
    "PartyB": "174379",
    "PhoneNumber": phone,
    "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
    "AccountReference": "account",
    "TransactionDesc": "account"
    }

    # POPULATING THE HTTP HEADER
    # Headers carry the access token and content type
    # JSON is the format of data
    headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json"
    }

    # SPECIFY SAFARICOM URL
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" # C2B URL

    # Finally, using requests, we post payload and headers to above url
    # Below code will automatically send a SIM TOOLKIT(stk) push to your phone

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

    # An API (Application Programming Interface) is a set of rules and protocols that allows one software application to interact with another. We are using Daraja to connect with the mpesa server.