from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import psycopg2

# initialize the app
app=Flask(__name__)
#base_directory=os.path.abspath(os.path.dirname(__file__))

#Initialize the database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Mango123@localhost/flask_test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
app.app_context().push()

#initialize marshmallow
ma=Marshmallow(app)

# class product (model)
class Product(db.Model):
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True)
    description=db.Column(db.String(200))
    price=db.Column(db.Float)
    quantity=db.Column(db.Integer)

    #constructor of the class
    def __init__(self,name,description,price,quantity):
        self.name=name
        self.description=description
        self.price=price
        self.quantity=quantity


# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields=('id','name','description','price','quantity')

#initialize schema
product_schema=ProductSchema()
products_schema=ProductSchema(many=True)

""""
# to create the db run the following commands
python
from app import db
db.create_all()
"""

# ........................... API end points ..............................

# add product
@app.route('/products',methods=['POST'])
def add_product():
    name=request.json['name']
    description=request.json['description']
    price=request.json['price']
    quantity=request.json['quantity']

    new_product=Product(name,description,price,quantity)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


#get all products
@app.route('/products',methods=['GET'])
def get_all_products():
    all_products=Product.query.all()
    result=products_schema.dump(all_products)
    return jsonify(result) # return an array of objects

# get a single product
@app.route('/products/<id>',methods=['GET'])
def get_product(id):
    product=Product.query.get(id)
    return product_schema.jsonify(product)

# update a product
@app.route('/products/<id>',methods=['PUT'])
def update_product(id):

    product=Product.query.get(id)
    name=request.json['name']
    description=request.json['description']
    price=request.json['price']
    quantity=request.json['quantity']

    product.name=name
    product.description=description
    product.price=price
    product.quantity=quantity

   
    db.session.commit()

    return product_schema.jsonify(product)


# delete product
@app.route('/products/<id>',methods=['DELETE'])
def delete_product(id):
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)





# run the app
if __name__=='__main__':
    app.run(debug=True)

