from django.shortcuts import render
from django.http import HttpResponse
import requests
from django import forms

from .forms import searchForm

from itertools import zip_longest

# Create your views here.


def located(request):
    params1 = {
        "access_key": "6eac61e32e037d550bbdd7ae8d26b8a4",
        "query": "Tehran",
    }

    params2 = {
        "latitude": "35.6944",
        "longitude": "51.4215",
        "current": "temperature_2m,apparent_temperature,is_day,weather_code,wind_speed_10m,wind_direction_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,wind_speed_10m_max",
        "timezone": "auto",
    }

    if request.method == "GET":
        form = searchForm()
        api1_result = requests.get("http://api.weatherstack.com/current", params1)
        api1_response = api1_result.json()
        city = api1_response["location"]["name"]
        ###############
        params2["latitude"] = api1_response["location"]["lat"]
        params2["longitude"] = api1_response["location"]["lon"]
        api2_result = requests.get("https://api.open-meteo.com/v1/forecast", params2)
        api2_response = api2_result.json()
        current = api2_response["current"]
        daily = zip_longest(
            api2_response["daily"]["time"],
            api2_response["daily"]["weather_code"],
            api2_response["daily"]["temperature_2m_max"],
            api2_response["daily"]["temperature_2m_min"],
            api2_response["daily"]["sunrise"][-5:],
            api2_response["daily"]["sunset"][-5:],
            api2_response["daily"]["wind_speed_10m_max"],
        )

        return render(
            request,
            "index.html",
            {
                "form": form,
                "city": city,
                "current": current,
                "daily": daily,
            },
        )

    if request.method == "POST":
        form = searchForm(request.POST)
        if not form.is_valid():
            return forms.ValidationError("the city is not correct")

        params1["query"] = form.cleaned_data["city"]
        api1_result = requests.get("http://api.weatherstack.com/current", params1)
        api1_response = api1_result.json()
        city = api1_response["location"]["name"]
        #############
        params2["latitude"] = api1_response["location"]["lat"]
        params2["longitude"] = api1_response["location"]["lon"]
        api2_result = requests.get("https://api.open-meteo.com/v1/forecast", params2)
        api2_response = api2_result.json()
        current = api2_response["current"]
        api2_response["daily"]["sunset"] = list(
            map(lambda x: x.split("T")[1], api2_response["daily"]["sunset"])
        )
        api2_response["daily"]["sunrise"] = list(
            map(lambda x: x.split("T")[1], api2_response["daily"]["sunrise"])
        )
        daily = zip_longest(
            api2_response["daily"]["time"],
            api2_response["daily"]["weather_code"],
            api2_response["daily"]["temperature_2m_max"],
            api2_response["daily"]["temperature_2m_min"],
            api2_response["daily"]["sunrise"],
            api2_response["daily"]["sunset"],
            api2_response["daily"]["wind_speed_10m_max"],
        )
        #############

        return render(
            request,
            "index.html",
            {
                "form": searchForm(),
                "city": city,
                "current": current,
                "daily": daily,
            },
        )
