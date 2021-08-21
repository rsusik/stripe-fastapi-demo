# Stripe payment using FastAPI

## Accept a payment (prebuilt checkout page using fastapi)

This code use [FastAPI](https://github.com/tiangolo/fastapi) and [Stripe](https://stripe.com/) for payments and is mostly based on [this example](https://github.com/stripe-samples/accept-a-payment/tree/main/prebuilt-checkout-page) which use [Flask](https://github.com/pallets/flask).

This repository includes example of Prebuilt Checkout page integration. Below is comparison of both methods.

### Methods

|**Prebuilt Checkout page** ([docs](https://stripe.com/docs/payments/accept-a-payment?ui=checkout))| **Custom payment flow** ([docs](https://stripe.com/docs/payments/accept-a-payment?ui=elements)) |
|---|---|
| Lower complexity. | Higher complexity. |
| Customize logo, images, and colors. | Customize all components with CSS. |
| Add payment method types with a single line change. | Implement each payment method type as a custom integration. |
| Built-in support for Apple Pay, and Google Pay. | Integrate Apple Pay and Google Pay with extra code.|
| Redirect to Stripe hosted page. | Customers stay on your site. |
| Small refactor to collect recurring payments. | Large refactor to collect recurring payments. |
| Input validation and error handling built in. | Implement your own input validation and error handling. |
| Localized in 25+ languages. | Implement your own localization. |


### Payment Method Type Support

|Payment Method Type | [Prebuilt Checkout page](./prebuilt-checkout-page) ([docs](https://stripe.com/docs/payments/accept-a-payment?ui=checkout))| [Custom payment flow](./custom-payment-flow) ([docs](https://stripe.com/docs/payments/accept-a-payment?ui=elements)) |
|---|---|---|
|ACH Credit Transfer|  |  |
|ACH Debit|  |  |
|Afterpay/Clearpay| ✅ | ✅ |
|Alipay| ✅ | ✅ |
|Apple Pay| ✅ | ✅ |
|Bacs Direct Debit| ✅ |  |
|Bancontact| ✅ | ✅ |
|BECS Direct Debit| | ✅ |
|Boleto| ✅ | ✅ |
|Cards| ✅ | ✅ |
|EPS| ✅ | ✅ |
|FPX| ✅ | ✅ |
|giropay| ✅ | ✅ |
|Google Pay| ✅ | ✅ |
|GrabPay| ✅ | ✅ |
|iDEAL| ✅ | ✅ |
|Klarna|  |  |
|Multibanco| | ✅ |
|OXXO| | ✅ |
|Przelewy24 (P24)| ✅ | ✅ |
|SEPA Direct Debit| ✅ | ✅ |
|Sofort| ✅ | ✅ |
|WeChat Pay|  |  |


### Installation
You'll find more detailed instructions for each integration type in the
relevant READMEs (links to original repo):

- [Prebuilt Checkout page](https://github.com/stripe-samples/accept-a-payment/tree/main/prebuilt-checkout-page/README.md)
- [Custom payment flow](https://github.com/stripe-samples/accept-a-payment/tree/main/custom-payment-flow/README.md)

## Origin

This code was originally based on Flask, and the source codes may be found at https://github.com/stripe-samples/accept-a-payment.
