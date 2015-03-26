__author__ = 'tunedconsulting@gmail.com'

from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy.orm.exc import NoResultFound

from libs.database_setup import Restaurant, MenuItem
from libs.dbSession import engine, start_session

session = start_session(engine)

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def start():
    """
    Diplay all the restaurants
    """
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/new/', methods=['GET', 'POST'])
def new_restaurant():
    """
    Create a new Restaurant instance in the database
    """
    if request.method == 'GET':
        return render_template('newrestaurant.html')
    elif request.method == 'POST':
        print request.form['name']
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        flash("new restaurant %s created!" % new_restaurant.name)
        return redirect(url_for('start'))

    return 404


@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    """
    Edit data about a Restaurant
    :param restaurant_id: id of a restaurant in the db
    """
    if request.method == 'GET':
        restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
        return render_template('editrestaurant.html', restaurant=restaurant)
    elif request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("%s edited!" % request.form['name'])
        return redirect(url_for('start'))

    return 404


@app.route('/restaurants/<int:restaurant_id>/remove/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    """
    Delete a Restaurant
    :param restaurant_id:
    """
    if request.method == 'GET':
        restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
        return render_template('deleterestaurant.html', restaurant=restaurant)
    elif request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
        session.delete(restaurant)
        session.commit()
        flash("restaurant %s deleted!" % restaurant.name)
        return redirect(url_for('start'))


@app.route('/restaurants/<int:restaurant_id>/', methods=['GET', 'POST'])
def list_items(restaurant_id):
    """
    Display the menu of a Restaurant
    :param restaurant_id: id of the restaurant
    """
    restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/edit/<int:item_id>/', methods=['GET', 'POST'])
def edit_item(restaurant_id, item_id):
    """
    Edit an item in Restaurant's menu
    :param restaurant_id: id of the restaurant
    :param item_id: id of the item
    """
    if request.method == 'GET':
        item = session.query(MenuItem).filter_by(id=int(item_id)).one()
        return render_template('editmenuitem.html', item=item)
    elif request.method == 'POST':
        item = session.query(MenuItem).filter_by(id=int(item_id)).one()
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        session.add(item)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for('list_items', restaurant_id=restaurant_id))

    return 404


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_item(restaurant_id):
    """
    Add a new MenuItem to a Restaurant menu
    :param restaurant_id:
    :return:
    """
    if request.method == 'GET':
        restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
        return render_template('newmenuitem.html', restaurant=restaurant)
    elif request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
        new_item = MenuItem(name=request.form['name'],
                            description=request.form['description'],
                            price=request.form['price'],
                            course=request.form['course'],
                            restaurant=restaurant)
        session.add(new_item)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('list_items', restaurant_id=restaurant_id))

    return 404

@app.route('/restaurants/<int:restaurant_id>/remove/<int:item_id>/', methods=['GET', 'POST'])
def delete_item(restaurant_id, item_id):
    """
    Delete a MenuItem from a Restaurant's menu
    :param restaurant_id: id of a restaurant
    :param item_id: id of a menu
    """
    if request.method == 'GET':
        item = session.query(MenuItem).filter_by(id=int(item_id)).one()
        return render_template('deletemenuitem.html', item=item)
    elif request.method == 'POST':
        item = session.query(MenuItem).filter_by(id=int(item_id)).one()
        session.delete(item)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('list_items', restaurant_id=restaurant_id))

    return 404


@app.route('/restaurants/JSON/', methods=['GET'])
def api_restaurants():
    """
    Returns a JSON containing all the restaurants
    :return: json
    """
    restaurants = session.query(Restaurant).all()
    return jsonify({"Restaurants": [r.serialize for r in restaurants]})


@app.route('/restaurants/<int:restaurant_id>/menu/JSON/', methods=['GET'])
def api_restaurant_menu(restaurant_id):
    """
    Returns a JSON containing all menu items of a Restaurant
    :param restaurant_id: id of the restaurant
    :return: json
    """
    try:
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    except NoResultFound:
        return jsonify({'error': 404, 'err': 'Wrong item id'})
    return jsonify({"MenuItems": [i.serialize for i in items]})


@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/JSON/', methods=['GET'])
def api_single_item(restaurant_id, item_id):
    """
    Returns a JSON containing the details of a single MenuItem
    :param restaurant_id: id of a Restaurant
    :param item_id: id of a MenuItem
    :return: json
    """
    try:
        item = session.query(MenuItem).filter_by(id=item_id).one()
    except NoResultFound:
        return jsonify({'error': 404, 'err': 'Wrong item id'})

    if item.restaurant.id != restaurant_id:
        return jsonify({'error': 404, 'err': 'Wrong item or restaurant ids'})

    return jsonify({"MenuItem": item.serialize})


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=5000)