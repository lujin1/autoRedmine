from flask import Blueprint, Response, request
from api.redmineSelenium import *
import json

redmine_api = Blueprint('redmine_api', __name__, url_prefix='/')


@redmine_api.route('/', methods=['POST'])
def runRedmine():
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    try:
        result = seleniumRedmine(username, password, name)
        msg = {
            "status": "success",
            "result": result,
            "action": "Run Redmine"
        }
        return Response(json.dumps(msg), content_type='application/json')
    except Exception as e:
        print(e)
        msg = {
            "status": "failed",
            "action": "Run Redmine",
            "error": str(e)
        }
        return Response(json.dumps(msg), content_type='application/json')

