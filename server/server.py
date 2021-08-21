#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

import os
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import stripe
from dotenv import load_dotenv, find_dotenv

# Setup Stripe python client library.
load_dotenv(find_dotenv())

# Ensure environment variables are set.
price = os.getenv('PRICE')
if price is None or price == 'price_12345' or price == '':
    print('You must set a Price ID in .env. Please see the README.')
    exit(0)

# For sample support and debugging, not required for production:
stripe.set_app_info(
    'stripe-samples/accept-a-payment/prebuilt-checkout-page',
    version='0.0.1',
    url='https://github.com/stripe-samples')

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = '2020-08-27'

static_dir = str(os.path.abspath(os.path.join(
    __file__, "..", os.getenv("STATIC_DIR"))))

templates = Jinja2Templates(directory=static_dir)

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get('/')
def get_example(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


# Fetch the Checkout Session to display the JSON result on the success page
@app.get('/checkout-session', response_model=stripe.checkout.Session)
def get_checkout_session(
    sessionId : str
):
    id = sessionId
    checkout_session = stripe.checkout.Session.retrieve(id)
    return checkout_session


@app.post('/create-checkout-session')
def create_checkout_session():
    domain_url = os.getenv('DOMAIN')
    try:
        # Create new Checkout Session for the order
        # Other optional params include:

        # For full details see https:#stripe.com/docs/api/checkout/sessions/create
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + '/static/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + '/static/canceled.html',
            payment_method_types=(os.getenv('PAYMENT_METHOD_TYPES') or 'card').split(','),
            mode='payment',
            line_items=[{
                'price': os.getenv('PRICE'),
                'quantity': 1,
            }]
        )
        return RedirectResponse(
            checkout_session.url, 
            status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        raise HTTPException(403, str(e))

class WebHookData(BaseModel):
    data : dict
    type : str

@app.post('/webhook')
def webhook_received(
    request_data : WebHookData,
    stripe_signature: Optional[str] = Header(None)
):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    # request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = stripe_signature
        try:
            event = stripe.Webhook.construct_event(
                payload=request_data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print('event ' + event_type)

    if event_type == 'checkout.session.completed':
        print('🔔 Payment succeeded!')
        # Note: If you need access to the line items, for instance to
        # automate fullfillment based on the the ID of the Price, you'll
        # need to refetch the Checkout Session here, and expand the line items:
        #
        # session = stripe.checkout.Session.retrieve(
        #     data['object']['id'], expand=['line_items'])
        #
        # line_items = session.line_items
        #
        # Read more about expand here: https://stripe.com/docs/expand
    return {'status': 'success'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=4242,
        # ssl_keyfile= Path(__file__).absolute().parents[0] / 'localhost.key',
        # ssl_certfile= Path(__file__).absolute().parents[0] / 'localhost.crt'
    )