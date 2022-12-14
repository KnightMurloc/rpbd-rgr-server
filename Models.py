from sqlalchemy import Integer, String, Column, DateTime, REAL, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Employees(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    patronymic = Column(String)
    birth_date = Column(DateTime)
    salary = Column(REAL)
    post = Column(Integer, ForeignKey("post.id"))
    address = Column(Integer, ForeignKey("address.id"))
    Post = relationship("Models.Post")
    Address = relationship("Models.Address")

    def __init__(self, data, session):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.patronymic = data["patronymic"]
        self.birth_date = data["birth_date"]
        self.salary = data["salary"]
        self.post = data["post"]["id"]
        self.Post = session.query(Post).get(data["post"]["id"])
        self.address = data["address"]["id"]
        self.Address = session.query(Address).get(data["address"]["id"])

    def to_json(self):
        result = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "patronymic": self.patronymic,
            "birth_date": str(self.birth_date),
            "salary": self.salary,
            "address": self.Address.to_json(),
            "post": self.Post.to_json()
        }
        return result


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    reason = Column(Text)
    order_number = Column(Integer)
    order_date = Column(DateTime)
    employer_id = Column("employer", Integer, ForeignKey("employees.id"))
    post_id = Column("post", Integer, ForeignKey("post.id"))
    Employer = relationship("Employees")
    Post = relationship("Post")

    def __init__(self, data, session):
        self.id = int(data["id"])
        self.reason = data["reason"],
        self.order_number = data["order_number"],
        self.order_date = data["order_date"],
        self.employer_id = data["Employer"]["id"],
        self.Employer = session.query(Employees).get(data["Employer"]["id"])
        self.post_id = data["Post"]["id"],
        self.Post = session.query(Post).get(data["Post"]["id"])

    def to_json(self):
        return {
            "id": self.id,
            "reason": self.reason,
            "order_number": self.order_number,
            "order_date": str(self.order_date),
            "Employer": self.Employer.to_json() if self.Employer is not None else None,
            "Post": self.Post.to_json()
        }


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit_id = Column("unit", Integer, ForeignKey("unit.id"))
    unit = relationship("Unit")

    def __init__(self, data, session):
        self.id = data["id"]
        self.name = data["name"]
        self.unit_id = data["unit"]["id"]
        self.unit = session.query(Unit).get(data["unit"]["id"])

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit.to_json()
        }


class Provider(Base):
    __tablename__ = "provider"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)
    fax = Column(String)
    email = Column(String)
    post_address_id = Column("address", Integer, ForeignKey('address.id'))

    post_address = relationship("Address")

    def __init__(self, data, session):
        self.id = data["id"]
        self.name = data["name"]
        self.phone_number = data["phone_number"]
        self.fax = data["fax"]
        self.email = data["email"]
        self.post_address_id = data["post_address"]["id"]
        self.post_address = session.query(Address).get(data["post_address"]["id"])

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "fax": self.fax,
            "email": self.email,
            "post_address": self.post_address.to_json(),
        }


"""
 id             | integer           |           | not null | nextval('products_id_seq'::regclass)
 ingredient     | integer           |           |          | 
 price          | real              |           | not null | 
 delivery_terms | character varying |           | not null | 
 payment_terms  | character varying |           | not null | 
 provider       | integer           |           |          | 
 name           | character varying |           |          | 

"""


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ingredient_id = Column("ingredient", Integer, ForeignKey("ingredients.id"))
    price = Column(REAL)
    delivery_terms = Column(Text)
    payment_terms = Column(Text)
    provider_id = Column("provider", Integer, ForeignKey("provider.id"))
    ingredient = relationship("Ingredient")
    provider = relationship("Provider")

    def __init__(self, data, session):
        self.id = data["id"]
        self.name = data["name"]
        self.ingredient_id = data["ingredient"]["id"]
        self.ingredient = session.query(Ingredient).get(data["ingredient"]["id"])
        self.price = data["price"]
        self.delivery_terms = data["delivery_terms"]
        self.payment_terms = data["payment_terms"]
        self.provider_id = data["provider"]["id"]
        self.provider = session.query(Provider).get(data["provider"]["id"])
        self.id = data["id"]

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredient": self.ingredient.to_json(),
            "price": self.price,
            "delivery_terms": self.delivery_terms,
            "payment_terms": self.payment_terms,
            "provider": self.provider.to_json() if self.provider is not None else None,
        }


class SnackRecipe(Base):
    __tablename__ = "SnackRecipes"
    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    count = Column(Integer)
    snack_id = Column(Integer, ForeignKey("Snack.id"))
    ingredient = relationship("Ingredient")
    snack = relationship("Snack")

    def to_json(self):
        return {
            "id": self.id,
            "ingredient": self.ingredient.to_json(),
            "count": self.count
            # "snack": self.snack.to_json(),

        }


class DrinkRecipe(Base):
    __tablename__ = "DrinkRecipes"
    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    count = Column(Integer)
    drink_id = Column(Integer, ForeignKey("Drink.id"))
    ingredient = relationship("Ingredient")
    drink = relationship("Drink")

    def to_json(self):
        return {
            "id": self.id,
            "ingredient": self.ingredient.to_json(),
            "count": self.count
        }


def get_recipe_snack(data, self_id, session):
    result = []

    for rep in data:
        if rep["id"] != 0 and rep["id"] is not None:
            result.append(session.query(SnackRecipe).get(rep["id"]))
        else:
            # rep["id"] = None
            rr = SnackRecipe()
            rr.ingredient = session.query(Ingredient).get(rep["ingredient"]["id"])
            rr.count = rep["count"]
            rr.snack = session.query(Snack).get(self_id)
            session.add(rr)
            session.commit()
            result.append(rr)
    return result


def get_recipe_drink(data, self_id, session):
    result = []

    for rep in data:
        if rep["id"] != 0 and rep["id"] is not None:
            result.append(session.query(DrinkRecipe).get(rep["id"]))
        else:
            # rep["id"] = None
            rr = DrinkRecipe()
            rr.ingredient = session.query(Ingredient).get(rep["ingredient"]["id"])
            rr.count = rep["count"]
            rr.snack = session.query(Drink).get(self_id)
            session.add(rr)
            session.commit()
            result.append(rr)
    return result


class Snack(Base):
    __tablename__ = "Snack"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(Integer)

    ingredients = relationship(lambda: SnackRecipe)

    def __init__(self, data, session):
        # print(data)
        self.id = data["id"]
        self.name = data["name"]
        self.size = data["size"]
        # ingredients = [session.query(SnackRecipe).get(rep["id"]) for rep in data["ingredients"]]
        # print(get_recipe_snack(data["ingredients"], self.id, session))
        self.ingredients = get_recipe_snack(data["ingredients"], self.id, session)

    def to_json(self):
        # print([ing.to_json() for ing in self.ingredients])
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "ingredients": [ing.to_json() for ing in self.ingredients]
        }


"""
 id        | integer                |           | not null | nextval('drink_id_seq'::regclass)
 name      | character varying(255) |           |          | 
 strength  | integer                |           |          | 
 size      | integer                |           |          | 
 container | character varying(255) |           |          | 

"""


class Drink(Base):
    __tablename__ = "Drink"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    strength = Column(Integer)
    size = Column(Integer)
    container = Column(String)

    ingredients = relationship(lambda: DrinkRecipe)

    def __init__(self, data, session):
        # print(data)
        self.id = data["id"]
        self.name = data["name"]
        self.strength = data["strength"]
        self.size = data["size"]
        self.container = data["container"]
        # print(get_recipe(data["ingredients"], self.id, session))
        self.ingredients = get_recipe_drink(data["ingredients"], self.id, session)

    def to_json(self):
        # print([ing.to_json() for ing in self.ingredients])
        return {
            "id": self.id,
            "name": self.name,
            "strength": self.strength,
            "size": self.size,
            "container": self.container,
            "ingredients": [ing.to_json() for ing in self.ingredients]
        }


"""
 id     | integer |           | not null | nextval('drink_orders_id_seq'::regclass)
 drink  | integer |           | not null | 
 waiter | integer |           | not null | 
 table_ | integer |           | not null | 
"""


class DrinkOrder(Base):
    __tablename__ = "drink_orders"
    id = Column(Integer, primary_key=True)
    drink_id = Column("drink", Integer, ForeignKey("Drink.id"))
    waiter_id = Column("waiter", Integer, ForeignKey("employees.id"))
    table = Column("table_", Integer)

    drink = relationship("Drink")
    waiter = relationship("Employees")

    def __init__(self, data, session):
        self.id = data["id"]
        self.drink_id = data["drink"]["id"]
        self.drink = session.query(Drink).get(data["drink"]["id"])
        self.waiter_id = data["waiter"]["id"]
        self.waiter = session.query(Employees).get(data["waiter"]["id"])
        self.table = data["table"]

    def to_json(self):
        return {
            "id": self.id,
            "drink": self.drink.to_json(),
            "waiter": self.waiter.to_json(),
            "table": self.table,
        }


class SnackOrder(Base):
    __tablename__ = "snack_orders"
    id = Column(Integer, primary_key=True)
    snack_id = Column("snack", Integer, ForeignKey("Snack.id"))
    waiter_id = Column("waiter", Integer, ForeignKey("employees.id"))
    table = Column("table_", Integer)

    snack = relationship("Snack")
    waiter = relationship("Employees")

    def __init__(self, data, session):
        self.id = data["id"]
        self.snack_id = data["snack"]["id"]
        self.snack = session.query(Snack).get(data["snack"]["id"])
        self.waiter_id = data["waiter"]["id"]
        self.waiter = session.query(Employees).get(data["waiter"]["id"])
        self.table = data["table"]

    def to_json(self):
        return {
            "id": self.id,
            "snack": self.snack.to_json(),
            "waiter": self.waiter.to_json(),
            "table": self.table,
        }


"""
 id                 | integer               |           | not null | nextval('bank_detail_id_seq'::regclass)
 bank_name          | character varying     |           | not null | 
 tin                | character varying(10) |           | not null | 
 settlement_account | character varying(20) |           | not null | 
 provider           | integer               |           |          | 
 city               | integer               |           |          | 
"""


class BankDetail(Base):
    __tablename__ = "bank_detail"
    id = Column(Integer, primary_key=True)
    bank_name = Column(String)
    TIN = Column("tin", String)
    settlement_account = Column(String)
    provider_id = Column("provider", Integer, ForeignKey("provider.id"))
    city_id = Column("city", Integer, ForeignKey("city.id"))

    provider = relationship("Provider")
    city = relationship("City")

    def __init__(self, data, session):
        self.id = data["id"]
        self.bank_name = data["bank_name"]
        self.TIN = data["TIN"]
        self.settlement_account = data["settlement_account"]
        self.provider_id = data["provider"]["id"]
        self.provider = session.query(Provider).get(data["provider"]["id"])
        self.city_id = data["city"]["id"]
        self.city = session.query(City).get(data["city"]["id"])

    def to_json(self):
        return {
            "id": self.id,
            "bank_name": self.bank_name,
            "TIN": self.TIN,
            "settlement_account": self.settlement_account,
            "provider": self.provider.to_json(),
            "city": self.city.to_json(),
        }


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, data, session):
        self.id = data["id"]
        self.name = data["name"]

    def to_json(self):
        return {
            "id": self.id,
            'name': self.name
        }


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, data, session):
        self.id = data["id"]
        self.name = data["name"]

    def to_json(self):
        return {
            "id": self.id,
            'name': self.name
        }


class Unit(Base):
    __tablename__ = "unit"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, data, session):
        self.id = data["id"]
        self.name = data["name"]

    def to_json(self):
        return {
            "id": self.id,
            'name': self.name
        }


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, data, session):
        self.id = data["id"]
        self.name = data["name"]

    def to_json(self):
        return {
            "id": self.id,
            'name': self.name
        }
