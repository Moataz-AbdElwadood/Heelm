from rest_framework import viewsets
from .models import Blog
from .serializers import BlogSerializer
import os
from django.core import serializers
from uuid import uuid4
from django.shortcuts import render
from openai import OpenAI
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View  
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import string
from rest_framework.generics import ListAPIView
import random




from rest_framework.decorators import api_view
from rest_framework.response import Response
from tafseer.config import GPTConfig
from tafseer.models import Blog, Subscription
from tafseer.tab.tab import create_payment, get_charge_status

@api_view(['POST'])
def ask(request):
    # TODO: check if any token available 
    #TODO: MAKE FREE FIRST TIME LOGIC AND DESIGN
    # TODO : GET THE CONTENT Dynamically from request
    question = request.data.get('content')  # Assuming the input from the client is sent as JSON with 'content' key
    user_token = request.data.get('token')
    print("user_token: " , user_token)

    if not question:
        return Response({"error": "No content provided"}, status=400)

    if not user_token:
        return Response({"error": "No token provided"}, status=400)


    if user_token != "X":
        try:
            user = Subscription.objects.get(token=user_token)

        except Subscription.DoesNotExist:
            # Handle the case where no matching record is found
            return Response({"error": "No user found For this token"}, status=400)
        
        if  user.isUsed:
                 return Response({"error": "Subscription expired"}, status=403)
        if user.payment_status != 'completed':
                return Response({"error": "Subscription Not activated"}, status=400)
        
        resp =try_ask_catch(question)
        return resp
    else:
       new_token=create_sub()
       resp =try_ask_catch(question,new_token)
       print("--------------------------------",resp.data)
    #    print("--------------------------------2",resp.data)
       return resp
        

   

def try_ask_catch(user_input,token):
    try:
        # Initialize OpenAI client
        client = OpenAI(
            api_key=GPTConfig.GPT_API_KEY
        )

        # Call the OpenAI GPT API with the user's input
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an experienced oneirocritic."},
                {"role": "user", "content": user_input}
            ]
        )

        # Check the status of the API response
        if completion and completion.choices:
            response_message = completion.choices[0].message.content
            # Return the response to the client
            return Response({ "status": "success","message":token,"data": response_message}, status=200)
        else:
            # If the API did not return a valid response
            return Response({"error": "Invalid response from GPT model"}, status=500)

    except Exception as e:
        # Handle any exceptions, such as network errors or issues with the OpenAI API
        return Response({"error": str(e)}, status=500)



def create_sub():
        user_id=uuid4()
        token=''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        subbing_data = {
            "id":user_id,
            "token":token,
            "isUsed":True,
        }

        subbing = Subscription.objects.create(**subbing_data)
        print("TOKEN -------->",token)
        # subbing.save()
        # Prepare the booking data to create a Booking object
        return subbing_data["token"]

#     // In your React component
# useEffect(() => {
#   fetch('http://localhost:8000/subapp/api/data/')
#     .then(response => response.json())
#     .then(data => console.log(data))
#     .catch(error => console.error('Error:', error));
# }, []);

@method_decorator(csrf_exempt, name='dispatch')   
class UpdateOrderStatusView(View):
    def post(self, request):
        print("INSIDE UpdateOrderStatusView")
        if request.method == 'POST':
            data = json.loads(request.body)
            print("---------UpdateOrderStatusView", data)
            # print("---------UpdateOrderStatusView", data['reference'])

            if data['status'] == 'CAPTURED':
                user_id = data['metadata']['user_id']
                try:
                    subbing = Subscription.objects.get(id=user_id) 
                    subbing.payment_status = 'completed'
                    print("sub completed",subbing)

                    # TODO: Generate new token for this user
                   
                    subbing.isUsed = False
                    subbing.save()
                except Subscription.DoesNotExist:
                    return JsonResponse({'error': 'Subscription not found'}, status=404)
            return JsonResponse({ "status": "success","message":"Done","data":''}, status=200)
        return JsonResponse({'error': 'Invalid request method'}, status=400)    
    


class PlaceEventOrderAPIView(APIView):

    def get_booking_creation_data(self, token):
        try:
            subbin = Subscription.objects.get(token=token)
            print("Subscription Found:", subbin)
            return subbin
        except Subscription.DoesNotExist:
            print("No subscription found for this token.")
            return None

    def get(self, request):
        # Get the token from the GET parameters
        token = request.GET.get('token')

        # Check if the token is provided
        if not token:
            return JsonResponse({'error': 'No token provided'}, status=400)

        # Fetch subscription data based on the token
        subbing_data = self.get_booking_creation_data(token)

        # Handle case where no subscription is found
        if subbing_data is None:
            return JsonResponse({'error': 'Invalid token'}, status=404)

        try:
            # Attempt to create a payment and get the payment URL
            payment_url = create_payment(request, subbing_data)
        except Exception as e:
            # Handle any potential errors from create_payment
            print("Payment creation error:", str(e))
            return JsonResponse({'error': 'Payment creation failed', 'details': str(e)}, status=500)

        # Ensure that a payment URL was generated
        if not payment_url:
            return JsonResponse({'error': 'Invalid payment data'}, status=400)

        # Return a success response with the payment URL
        return JsonResponse({"status": "success", "message": "Redirect Link", "data": payment_url}, status=200)

@method_decorator(csrf_exempt, name='dispatch') 
class CheckChargeStatusView(View):
    def get(self, request, tap_id):
        status, customer_name = get_charge_status(tap_id)
        if status == 'success':  # Replace with actual check
            return JsonResponse({'status': 'success', 'customer_name': customer_name})
        else:
            return JsonResponse({'status': 'failure', 'customer_name': customer_name})
        


# List all blogs
class BlogViewSet(ListAPIView):
    serializer_class = BlogSerializer  # Define the serializer class

    def get_queryset(self):
        # Return the queryset of blog objects, ordered by creation date
        return Blog.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        # Get the queryset
        queryset = self.get_queryset()

        # Serialize the queryset
        serializer = BlogSerializer(queryset, many=True)

        # Return a JSON response
        return JsonResponse({
            "status": "success",
            "message": "Blogs fetched successfully",
            "data": serializer.data
        }, status=200)