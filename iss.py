#!/usr/bin/env python

__author__ = 'Albina Tileubergen-Thomas'

import requests
import turtle
import time

world_map = "map.gif"
iss_image = "iss.gif"
iss_url = "http://api.open-notify.org"


def get_astronauts_list():
    res = requests.get(iss_url + "/astros.json")
    astronaut_info = res.json()["people"]
    astronaut_number = res.json()["number"]
    print(
        f'Total list of astronauts are: {astronaut_number}')
    for each_dict in astronaut_info:
        for key in each_dict:
            if key == "name":
                list_astro = each_dict.get(key)
                print(list_astro)


def iss_location():
    res = requests.get(iss_url + "/iss-now.json")
    location = res.json()["iss_position"]
    lat = float(location["latitude"])
    lon = float(location["longitude"])
    print(f'Current ISS coordinates: lat: {lat}, lon: {lon}')
    return lat, lon
    # for k, v in location.items():
    #     print(f"{k}: {v}")


def iss_map(lat, lon):
    screen = turtle.Screen()
    screen.setup(1000, 600)
    screen.bgpic(world_map)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.register_shape(iss_image)

    iss = turtle.Turtle()
    iss.shape(iss_image)
    iss.setheading(90)
    iss.penup()
    iss.goto(lon, lat)
    return screen


def indi_pass_time(lat, lon):
    params = {'lat': lat, 'lon': lon}
    res = requests.get(iss_url + "/iss-pass.json", params=params)
    passover_time = res.json()['response'][1]['risetime']
    return time.ctime(passover_time)


def main():
    get_astronauts_list()
    lat, lon = iss_location()

    screen = iss_map(lat, lon)
    indi_lat = 39.768403
    indi_lon = -86.158068
    location = turtle.Turtle()
    location.penup()
    location.color("yellow")
    location.goto(indi_lon, indi_lat)
    location.dot(5)
    location.hideturtle()
    next_passover = indi_pass_time(indi_lat, indi_lon)
    location.write(next_passover, align="center",
                   font=("Helvetice", 14, "normal"))

    if screen is not None:
        print("Click Screen to exit :)")
        screen.exitonclick()


if __name__ == '__main__':
    main()
