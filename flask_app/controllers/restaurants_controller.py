from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.restaurants_model import Restaurant
from flask_app.models.users_model import User


# @app.route('/')
# def home():
#     return render_template('dashboard.html')

# this route will show the restaurants in the data base onto the home page
@app.route('/')
def show_restaurants():

    many_restaurants = Restaurant.get_all_restaurants()
    print(many_restaurants)
    return render_template('dashboard.html' , many_restaurants=many_restaurants)


# This will show the one restaurant page
@app.route('/<restaurant_name>/<int:restaurant_id>')
def show_one_restaurant(restaurant_name, restaurant_id):

    one_restaurant = Restaurant.get_one_restaurant({'restaurant_id' : restaurant_id})

    return render_template('one_restaurant.html', one_restaurant=one_restaurant)
