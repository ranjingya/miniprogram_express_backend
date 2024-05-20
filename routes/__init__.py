from flask import Flask, jsonify, request, g, make_response
from jwt import ExpiredSignatureError
from pymongo import MongoClient
import redis, requests, os, jwt, socket, time, random, string


app = Flask(__name__,
            template_folder="../templates",
            static_folder="../assets",
            static_url_path="/assets")

app.json.ensure_ascii = False  # 解决中文乱码问题

from routes import express_routes
from routes import weather_routes
from routes import login_routes
from interceptor import login_interceptor