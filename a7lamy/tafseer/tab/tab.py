
from tafseer.tab.config import TapConfig
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import requests

def get_post_hook_url(request):

        current_site = "7b84-156-181-98-161.ngrok-free.app/"
        post_hook_path = reverse('update-order-status')
        return f'https://{current_site}{post_hook_path}'


def get_redirect_url():
        # TODO: make it frontend domaing not current site
        current_site = "7b84-156-181-98-161.ngrok-free.app/"
        return f'https://a7lamy.vercel.app/'


def create_payment(request, subbing):
    if not subbing:
         return None
    user_id=str(subbing.id)

    url = f"{TapConfig.API_BASE_URL}/v2/charges"
    headers = {
        "Authorization": f"Bearer {TapConfig.API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "amount": float(2),
        "currency": "SAR",
        "description": f"Subbing for one request",
        "source": {"id": "src_all"},
        "customer": {
            #  TODO: generate random name and email
            "first_name": "John Doe",
            "email": "john.doe@gmail.com",
        },
        "post": {
                "url": get_post_hook_url(user_id)  # Dynamic post hook URL
        },
        "redirect": {
            "url": get_redirect_url()
        },
        "reference": {
            "user_id": str(user_id)
        },
        "metadata":{
            "user_id": str(user_id)
        }
    }  
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        payment_url = response.json()["transaction"]["url"]

        return payment_url
    else:

        raise Exception("Payment creation failed")

# awl ma ed5ol elserver lazm a5od el ip bta3o we a7olto el limite = 1 we da el default  api for auth
# api to generate tafseer based on the limit that this IP has in his

# api to payment that if successful bezawd el limit ely fel table 1 
# create model for users that has, 1- IP. 2- Limit. 3- Name Optional. 
def get_charge_status(tap_id):

    url = f"{TapConfig.API_BASE_URL}/v2/charges/{tap_id}"
    headers = {
        "Authorization": f"Bearer {TapConfig.API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("status", "failure") == "CAPTURED":
            return 'success'
        return 'failure'
    else:
        return 'failure', ''