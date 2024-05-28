from flask import Flask, jsonify, request, g, make_response, Blueprint
from jwt import ExpiredSignatureError
from pymongo import MongoClient
import redis, requests, os, jwt, socket, time, random, string
from datetime import datetime
from routes.cart_routes import cart
from routes.goods_routes import goods
from routes.address_routes import address
from routes.send_routes import send

app = Flask(__name__,
            template_folder="../templates",
            static_folder="../assets",
            static_url_path="/assets")


app.json.ensure_ascii = False  # 解决中文乱码问题
app.register_blueprint(cart, url_prefix='/cart')
app.register_blueprint(goods, url_prefix='/goods')
app.register_blueprint(address, url_prefix='/address')
app.register_blueprint(send, url_prefix='/send')

from routes import express_routes
from routes import weather_routes
from routes import login_routes
from routes import cart_routes
from routes import goods_routes
from routes import address_routes
from routes import send_routes
from interceptor import login_interceptor