#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from flask import Flask
from flask_restful import Resource, Api,reqparse
from query import local_query,config

app = Flask(__name__)
api = Api(app)

class Query(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ip_str", type=str, required=True)
        self.parser.add_argument("token", type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        ip_str = args.ip_str
        token = args.token
        if token == config["本地"]["token"]:
            return local_query(ip_str)
        else:
            return {}

api.add_resource(Query, '/query')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,threaded=True)
