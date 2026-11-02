# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, analyze_review_sentiments, post_review
from .models import CarModel
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body)
        username = data["userName"].strip()
        password = data["password"]
        if not username or len(password) < 8:
            return JsonResponse({"error": "A username and password of at least 8 characters are required"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=409)
        user = User.objects.create_user(username=username, email=data.get("email", ""), password=password)
        login(request, user)
        return JsonResponse({"userName": user.username, "status": "Authenticated"}, status=201)
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "Invalid registration data"}, status=400)

def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    try:
        return JsonResponse({"status": 200, "dealers": get_request(endpoint)})
    except Exception as error:
        logger.exception("Unable to fetch dealerships: %s", error)
        return JsonResponse({"status": 502, "error": "Dealer service unavailable"}, status=502)


def get_dealer_details(request, dealer_id):
    try:
        return JsonResponse({"status": 200, "dealer": get_request(f"/fetchDealer/{dealer_id}")})
    except Exception as error:
        logger.exception("Unable to fetch dealer: %s", error)
        return JsonResponse({"status": 502, "error": "Dealer service unavailable"}, status=502)


def get_dealer_reviews(request, dealer_id):
    try:
        reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
        for review in reviews:
            review["sentiment"] = analyze_review_sentiments(review.get("review", "")).get("sentiment", "neutral")
        return JsonResponse({"status": 200, "reviews": reviews})
    except Exception as error:
        logger.exception("Unable to fetch dealer reviews: %s", error)
        return JsonResponse({"status": 502, "error": "Review service unavailable"}, status=502)


@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"}, status=403)
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "POST required"}, status=405)
    try:
        data = json.loads(request.body)
        data["name"] = request.user.username
        result = post_review(data)
        return JsonResponse({"status": 200, "review": result})
    except (ValueError, TypeError):
        return JsonResponse({"status": 400, "message": "Invalid review data"}, status=400)
    except Exception as error:
        logger.exception("Unable to post review: %s", error)
        return JsonResponse({"status": 502, "message": "Review service unavailable"}, status=502)


def get_cars(request):
    cars = [
        {"CarMake": car.car_make.name, "CarModel": car.name, "CarYear": car.year}
        for car in CarModel.objects.select_related("car_make").order_by("car_make__name", "name")
    ]
    return JsonResponse({"status": 200, "CarModels": cars})
