import ast
from random import choice
from typing import ValuesView
from django import http
from django.views.decorators.csrf import csrf_exempt
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
import requests
import json
import stripe
import time
from .models import Stripe_Data
from django.http import JsonResponse
from django.conf import settings
from django.views.generic.base import TemplateView

from django.core.exceptions import SuspiciousOperation
stripe.api_key = settings.STRIPE_SECRET_KEY # new
# Create your views here.

def json_list(request):
    
    api_resp = requests.get('https://fakestoreapi.com/products')
    api_resp_data = api_resp.json()
    
    return render(request, "index.html", {"api_resp_data":api_resp_data})
    
    
class success_payment(TemplateView):
        template_name = 'success_payment.html'
    
class cancel_payment(TemplateView):
    template_name = 'cancel_payment.html'

def order(request):
    queryset = Stripe_Data.objects.all() # list of objects
    # print(type(queryset))
    
    context = {
        'objects': queryset
    }
    return render(request, "order.html", context)

PRODUCTS_STRIPE_PRICING = {
    '1': 'price_1JBFOOSIOIKz7cmfFoRM41Nh',
    '2': 'price_1JBFOiSIOIKz7cmfcyOc3A4S',
    '3': 'price_1JBFPASIOIKz7cmf3ClugCH3',
    '4': 'price_1JBFPUSIOIKz7cmfcWLtxCCZ',
    '5': 'price_1JBFPmSIOIKz7cmfk1e0JXUf',
    '6': 'price_1JBFQ5SIOIKz7cmfuMw5p9zy',
    '7': 'price_1JBFQNSIOIKz7cmfLaCpfbKv',
    '8': 'price_1JBFQdSIOIKz7cmf801HDmFb',
    '9': 'price_1JBFQsSIOIKz7cmfkAMeTHA7',
    '10': 'price_1JBFRBSIOIKz7cmf4GHUSO9P',
    '11': 'price_1JBFRSSIOIKz7cmfi9TSkPao',
    '12': 'price_1JBFRgSIOIKz7cmfDDIj91iI',
    '13': 'price_1JBFS2SIOIKz7cmfeATOXnW1',
    '14': 'price_1JBFSFSIOIKz7cmfBDDSZkWF',
    '15': 'price_1JBFSXSIOIKz7cmfquEyOVL4',
    '16': 'price_1JBFSrSIOIKz7cmfMuLp0y42',
    '17': 'price_1JBFT6SIOIKz7cmfe41t56Qx',
    '18': 'price_1JBFTKSIOIKz7cmf9T9z0sOH',
    '19': 'price_1JBFTbSIOIKz7cmfacgmZBHs',
    '20': 'price_1JBFTsSIOIKz7cmfVf7bbNQz',
}
@csrf_exempt
def create_stripe_checkout_session(request, product_name):
    api_url = f"https://fakestoreapi.com/products/{product_name}"
    API_DATA = requests.get(api_url)
    global resp_api_data
    resp_api_data = API_DATA.json()
    # resr = resp_api_data['price']
    # print(resr)
    try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],

            metadata={'product_name': product_name, },
            line_items=[
                {'price': PRODUCTS_STRIPE_PRICING[product_name], 'quantity': 1, },
            ],
            mode='payment',
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            success_url='http://localhost:8000/success_payment.html',
            cancel_url='http://localhost:8000/cancel_payment.html',
            )

            return JsonResponse({'sessionId': checkout_session['id']})

    except Exception as e:
            print(e)
            raise SuspiciousOperation(e)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    payload = request.body.decode("UTF-8")
    payload_dictionary = json.loads(payload)
    # payload_dictionary_payment_status = payload_dictionary['data']['object']['id'] #to access  dictionary  sub-elements
    # payload_dictionary_payment_id = payload_dictionary['id'] #to access dictionary objects elements
    # print(payload_dictionary_payment_status)
    email = payload_dictionary['data']['object']['customer_details']['email'],
    email_s = ''.join(email)
    paymment_status = payload_dictionary['data']['object']['payment_status'],
    paymment_status_s = ''.join(paymment_status)
    transaction_id = payload_dictionary['data']['object']['payment_intent'],
    transaction_id_s = ''.join(transaction_id)
    price = payload_dictionary['data']['object']['amount_subtotal']
    
    # print(email_s)
    # print(payload_dictionary)
    # print(paymment_status_s)
    # print(transaction_id_s)
    # print(price)
    # print(type(payload_dictionary))
    # print(payload_dictionary)
    image = resp_api_data ['image']
    
    value = Stripe_Data(
        model_email = email_s,
        model_paymment_status = paymment_status_s,
        model_transaction_id = transaction_id_s,
        model_price = price, 
        model_image = image
        )
    value.save()
    # data = Stripe_Data.objects.get(id = 1)
    # print(data)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
        
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    print(event['type'])
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)