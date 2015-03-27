
from sqlalchemy.orm import sessionmaker, Query
from libs.database_setup import engine, Base, Restaurant, MenuItem


def create_sqlite_file(eng):
    Base.metadata.create_all(eng)


def start_session(eng):
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=eng)
    session = DBSession()
    return session


def insert_mock_data(ssn):
    my_first_restaurant = Restaurant(name="Pizza Palace")
    pizza_mozzarella = MenuItem(name="Pizza Mozzarella", description="Natural tomato sauce and mozzarella",
                                course="Entree", price="8.99$", restaurant=my_first_restaurant)
    ssn.add(pizza_mozzarella)
    ssn.add(my_first_restaurant)
    ssn.commit()


def query_restaurants_all(ssn):
    for q in ssn.query(Restaurant).all():
        print q.name


def query_filter_by(ssn, name=None, item_id=None):
    if name:
        return ssn.query(MenuItem).filter_by(name=name)
    elif item_id:
        return ssn.query(MenuItem).filter_by(id=item_id).one()
    else:
        raise AttributeError


def return_info_from_items(query):
    if isinstance(query, Query):
        if query.count() == 1:
            q = query
            print q.id
            print q.price
            print q.restaurant.name
            print "\n"
        else:
            for q in query:
                print q.id
                print q.price
                print q.restaurant.name
                print "\n"
    else:
        raise TypeError


def update_item_price(ssn, query, new_price):
    if query.count() == 1:
        query.price = new_price
        ssn.add(query)
        return ssn.commit()
    else:
        query = query
        for q in query:
            q.price = new_price
            ssn.add(q)
        return ssn.commit()




create_sqlite_file(engine)
session = start_session(engine)
################
#insert_mock_data(session)
#query_restaurants_all(session)
q = query_filter_by(session, name='Veggie Burger')
return_info_from_items(q)
#################

#################
#q1 = query_filter_by(session, item_id=10)
#return_info_from_items(q1)
#
#update_item_price(session, q1, '2.99$')
#
#q1 = query_filter_by(session, item_id=10)
#return_info_from_items(q1)
#################

#################
#q2 = query_filter_by(session, name='Veggie Burger')
#update_item_price(session, q2, '2.99$')
#################