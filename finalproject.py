__author__ = 'tunedconsulting@gmail.com'

from flask import Flask, render_template, request, url_for, redirect, flash, jsonify

from libs.database_setup import Restaurant, MenuItem
from libs.dbSession import engine, start_session

session = start_session(engine)

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def start():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
    return render_template('editrestaurant.html', restaurant=restaurant)


@app.route('/restaurants/new/', methods=['GET', 'POST'])
def new_restaurant():
    return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/remove/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
    return render_template('deleterestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/', methods=['GET', 'POST'])
def list_items(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/edit/<int:item_id>/', methods=['GET', 'POST'])
def edit_item(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=int(item_id)).one()
    return render_template('editmenuitem.html', item=item)


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
    return render_template('newmenuitem.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/remove/<int:item_id>/', methods=['GET', 'POST'])
def delete_item(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=int(item_id)).one()
    return render_template('deletemenuitem.html', item=item)


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=5000)