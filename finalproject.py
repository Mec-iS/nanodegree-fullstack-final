__author__ = 'tunedconsulting@gmail.com'

from flask import Flask, render_template, request, url_for, redirect, flash, jsonify

from libs.database_setup import Restaurant, MenuItem
from libs.dbSession import engine, start_session

session = start_session(engine)

app = Flask(__name__)


# Mocks: Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/restaurants')
def start():
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    return ' this is view 2 '


@app.route('/restaurants/new/', methods=['GET', 'POST'])
def new_restaurant():
    return ' this is view 3 '


@app.route('/restaurants/<int:restaurant_id>/remove/', methods=['GET', 'POST'])
def remove_restaurant(restaurant_id):
    return ' this is view 4 '


@app.route('/restaurants/<int:restaurant_id>/', methods=['GET', 'POST'])
def list_items(restaurant_id):
    return ' this is view 5 '


@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_item(restaurant_id):
    return ' this is view 6 '


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_item(restaurant_id):
    return ' this is view 7 '


@app.route('/restaurants/<int:restaurant_id>/remove/', methods=['GET', 'POST'])
def remove_item(restaurant_id):
    return ' this is view 8 '


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=5000)