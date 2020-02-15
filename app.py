import http
import os

import flask
import flask_sqlalchemy
import flask_marshmallow
import flask_wtf
import wtforms
from wtforms import validators

# 1 Init web application
app = flask.Flask(__name__)


# 2 Base routing and templates
@app.route('/home/', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return flask.render_template('home.html')


@app.route('/about/', methods=['GET'])
def about():
    return flask.render_template('about.html')


# 3 Forms
app.config['SECRET_KEY'] = 'random_string_for_safe'


class CreateProductForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(
        'Name',
        validators=[
            validators.DataRequired(),
            validators.Length(min=2, max=20),
        ]
    )
    description = wtforms.StringField(
        'Description',
        validators=[validators.DataRequired()]
    )
    price = wtforms.FloatField(
        'Price',
        validators=[
            validators.DataRequired(),
            validators.NumberRange(min=1, max=10000)
        ]
    )
    qty = wtforms.IntegerField(
        'Quantity',
        validators=[validators.DataRequired()]
    )
    submit = wtforms.SubmitField('Add product')


@app.route('/add_product/', methods=['GET', 'POST'])
def add_product():
    form = CreateProductForm()
    if form.validate_on_submit():
        flask.flash("Product successfully added", "success")
        print(form.name.data)
        print(form.description.data)
        print(form.price.data)
        print(form.qty.data)
        return flask.redirect(flask.url_for('home'))
    return flask.render_template('product_form.html', form=form)


# 4 Setup database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_NAME = 'flask_example_db.sqlite'
DB_URI = 'sqlite:///' + os.path.join(BASE_DIR, DB_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = flask_sqlalchemy.SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# 5 Setup marshmalos
ma = flask_marshmallow.Marshmallow(app)


class ProductSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'price',
            'qty'
        )


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# 6 Build api
@app.route('/products/', methods=['POST'])
def create_product():
    name = flask.request.json['name']
    description = flask.request.json['description']
    price = flask.request.json['price']
    qty = flask.request.json['qty']

    obj = Product(name, description, price, qty)
    db.session.add(obj)
    db.session.commit()

    return product_schema.jsonify(obj)


@app.route('/products/', methods=['GET'])
def list_product():
    queryset = Product.query.all()
    return products_schema.jsonify(queryset)


@app.route('/products/<id>/', methods=['GET'])
def retrieve_product(id):
    obj = Product.query.get(id)
    return product_schema.jsonify(obj)


@app.route('/products/<id>/', methods=['PUT'])
def update_product(id):
    obj = Product.query.get(id)

    name = flask.request.json['name']
    description = flask.request.json['description']
    price = flask.request.json['price']
    qty = flask.request.json['qty']

    obj.name = name
    obj.description = description
    obj.price = price
    obj.qty = qty

    db.session.commit()
    return product_schema.jsonify(obj)


@app.route('/products/<id>/', methods=['DELETE'])
def delte_product(id):
    obj = Product.query.get(id)
    db.session.delete(obj)
    db.session.commit()

    return '', http.HTTPStatus.NO_CONTENT


# Run demo server


if __name__ == '__main__':
    app.run(debug=True)
