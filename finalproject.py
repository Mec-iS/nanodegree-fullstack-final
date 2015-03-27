from random import random
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, g, session, abort
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.github import GitHub

from libs.database_setup import Restaurant, MenuItem, User
from libs.database_setup import engine, start_session
from libs.secret import secret_key, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

#
# This is a Flask Web-App
#

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = GITHUB_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = GITHUB_CLIENT_SECRET


# CSRF token
def generate_csrf_token():
    if '_csrf_token' not in session:
        rand = str(random())
        session['_csrf_token'] = rand
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

# set up github-flask
github = GitHub(app)

# database session
db_session = start_session(engine)

#
# Basic Routes
#


@app.route('/')
@app.route('/restaurants/')
def start():
    """
    Display all the restaurants
    """
    if g.user:
        restaurants = db_session.query(Restaurant).all()
        return render_template('restaurants.html', restaurants=restaurants, user=g.user)
    else:
        return render_template('restaurants.html', restaurants=[], user=None)


@app.route('/restaurants/new/', methods=['GET', 'POST'])
def new_restaurant():
    """
    Create a new Restaurant instance in the database
    """
    if g.user:
        if request.method == 'GET':
            return render_template('newrestaurant.html', user=g.user)
        elif request.method == 'POST':
            print request.form['name']
            new_restaurant = Restaurant(name=request.form['name'])
            db_session.add(new_restaurant)
            db_session.commit()
            flash("new restaurant %s created!" % new_restaurant.name)
            return redirect(url_for('start'))

        return 404

    return error_401()


@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    """
    Edit data about a Restaurant
    :param restaurant_id: id of a restaurant in the db
    """
    if g.user:
        if request.method == 'GET':
            restaurant = db_session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
            return render_template('editrestaurant.html', restaurant=restaurant, user=g.user)
        elif request.method == 'POST':
            restaurant = db_session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
            restaurant.name = request.form['name']
            db_session.add(restaurant)
            db_session.commit()
            flash("%s edited!" % request.form['name'])
            return redirect(url_for('start'))

        return 404

    return error_401()


@app.route('/restaurants/<int:restaurant_id>/remove/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    """
    Delete a Restaurant
    :param restaurant_id:
    """
    if g.user:
        if request.method == 'GET':
            restaurant = db_session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
            return render_template('deleterestaurant.html', restaurant=restaurant, user=g.user)
        elif request.method == 'POST':
            restaurant = db_session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
            items = db_session.query(MenuItem).filter_by(restaurant_id=int(restaurant_id)).all()
            for i in items:
                db_session.delete(i)
            db_session.delete(restaurant)
            db_session.commit()
            flash("restaurant %s deleted!" % restaurant.name)
            return redirect(url_for('start'))

    return error_401()


@app.route('/restaurants/<int:restaurant_id>/', methods=['GET', 'POST'])
def list_items(restaurant_id):
    """
    Display the menu of a Restaurant
    :param restaurant_id: id of the restaurant
    """
    if g.user:
        restaurant = db_session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
        items = db_session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        return render_template('menu.html', restaurant=restaurant, items=items, user=g.user)

    return error_401()


@app.route('/restaurants/<int:restaurant_id>/edit/<int:item_id>/', methods=['GET', 'POST'])
def edit_item(restaurant_id, item_id):
    """
    Edit an item in Restaurant's menu
    :param restaurant_id: id of the restaurant
    :param item_id: id of the item
    """
    if g.user:
        if request.method == 'GET':
            item = db_session.query(MenuItem).filter_by(id=int(item_id)).one()
            return render_template('editmenuitem.html', item=item, user=g.user)
        elif request.method == 'POST':
            item = db_session.query(MenuItem).filter_by(id=int(item_id)).one()
            item.name = request.form['name']
            item.description = request.form['description']
            item.price = request.form['price']
            db_session.add(item)
            db_session.commit()
            flash("menu item edited!")
            return redirect(url_for('list_items', restaurant_id=restaurant_id))

        return 404

    return error_401()


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_item(restaurant_id):
    """
    Add a new MenuItem to a Restaurant menu
    :param restaurant_id:
    """
    if g.user:
        if request.method == 'GET':
            restaurant = db_session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
            return render_template('newmenuitem.html', restaurant=restaurant, user=g.user)
        elif request.method == 'POST':
            restaurant = db_session.query(Restaurant).filter_by(id=int(restaurant_id)).one()
            new_item = MenuItem(name=request.form['name'],
                                description=request.form['description'],
                                price=request.form['price'],
                                course=request.form['course'],
                                restaurant=restaurant)
            db_session.add(new_item)
            db_session.commit()
            flash("new menu item created!")
            return redirect(url_for('list_items', restaurant_id=restaurant_id))

        return 404

    return error_401()

@app.route('/restaurants/<int:restaurant_id>/remove/<int:item_id>/', methods=['GET', 'POST'])
def delete_item(restaurant_id, item_id):
    """
    Delete a MenuItem from a Restaurant's menu
    :param restaurant_id: id of a restaurant
    :param item_id: id of a menu
    """
    if g.user:
        if request.method == 'GET':
            item = db_session.query(MenuItem).filter_by(id=int(item_id)).one()
            return render_template('deletemenuitem.html', item=item, user=g.user)
        elif request.method == 'POST':
            item = db_session.query(MenuItem).filter_by(id=int(item_id)).one()
            db_session.delete(item)
            db_session.commit()
            flash("menu item deleted!")
            return redirect(url_for('list_items', restaurant_id=restaurant_id))

        return 404

    return error_401()


#
# API Routes
#


@app.route('/api/restaurants/', methods=['GET'])
def api_restaurants():
    """
    Returns a JSON containing all the restaurants
    :return: json
    """
    restaurants = db_session.query(Restaurant).all()
    return jsonify({"Restaurants": [r.serialize for r in restaurants]})


@app.route('/api/restaurants/<int:restaurant_id>/menu/', methods=['GET'])
def api_restaurant_menu(restaurant_id):
    """
    Returns a JSON containing all menu items of a Restaurant
    :param restaurant_id: id of the restaurant
    :return: json
    """
    try:
        items = db_session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    except NoResultFound:
        return jsonify({'error': 404, 'err': 'Wrong item id'})
    return jsonify({"MenuItems": [i.serialize for i in items]})


@app.route('/api/restaurants/<int:restaurant_id>/menu/item/<int:item_id>/', methods=['GET'])
def api_single_item(restaurant_id, item_id):
    """
    Returns a JSON containing the details of a single MenuItem
    :param restaurant_id: id of a Restaurant
    :param item_id: id of a MenuItem
    :return: json
    """
    try:
        item = db_session.query(MenuItem).filter_by(id=item_id).one()
    except NoResultFound:
        return jsonify({'error': 404, 'err': 'Wrong item id'})

    if item.restaurant.id != restaurant_id:
        return jsonify({'error': 404, 'err': 'Wrong item or restaurant ids'})

    return jsonify({"MenuItem": item.serialize})


#
# Authentication & Authorization Routes
# https://github.com/cenkalti/github-flask/blob/master/example.py
#

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = db_session.query(User).get(session['user_id'])
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return error_401()


@app.after_request
def after_request(response):
    db_session.close()
    return response


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('start')
    if access_token is None:
        return redirect(next_url)

    user = db_session.query(User).filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db_session.add(user)
    user.github_access_token = access_token
    db_session.commit()

    session['user_id'] = user.id
    flash("Welcome!")
    return redirect(url_for('start'))


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        flash("Already logged in.")
        return redirect(url_for('start'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.")
    return redirect(url_for('start'))


@app.route('/user')
def user():
    flash("Hi, " + str(github.get('user')['name']))
    return redirect(url_for('start'))


#
# Custom Auth Error
# http://stackoverflow.com/questions/7877230/standard-401-response-when-using-http-auth-in-flask
#


@app.errorhandler(401)
def error_401(error=401):
    flash("You must login to access this page.")
    return redirect(url_for('start'))


if __name__ == '__main__':
    app.secret_key = secret_key
    app.debug = True
    app.run(host='127.0.0.1', port=5000)