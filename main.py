# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, jsonify, json, g
from flask_restful import Resource, Api, reqparse, request
from flask_jwt_router import JwtRoutes
from google.cloud import firestore
from google.cloud.firestore_v1 import document
import utilities
import project1 as p1
import os
import sys
import subprocess
import datetime
import jwt


class Package(object):
    def __init__(self, metadata, data):
        self.metadata = metadata
        self.data = data

    def to_dict(self):
        package = {
            'metadata' : self.metadata,
            'data' : self.data
        }
        return package

    def __repr__(self):
        return 'Package(metadata={}, data={}, priority={})'.format(self.metadata, self.data)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
db = firestore.Client()
api = Api(app)
# JwtRoutes(app)
# jwt_routes = JwtRoutes()

app.config['SECRET_KEY'] = 'this is my secret token'

# class UserModel(db.Model):
#     user_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)

class PackageList(Resource):
    # Get all packages on one big page
    @app.route("/packages", methods = ['POST'])
    def getPackages():
        try:
            offset = request.args.get('offset')
            if offset == None:
                offset = 1
            else:
                offset = int(offset)
            # print("offset: " + offset)
            packages_ref = db.collection('packages')
            docs = packages_ref.stream()
            packages = []
            counter = 1
            for doc in docs:
                if((counter > ((offset - 1) * 10)) and (counter <= (offset * 10))):
                    packages.append(doc.to_dict()['metadata'])
                counter += 1

            return jsonify(packages)
        except: return jsonify(code=0, message='Unexpected error retrieving packages')

    # Create/Ingest package
    @app.route("/package", methods = ['POST'])
    def createPackage():
        try:
            args = parser.parse_args()
            package = Package(metadata=args['metadata'], data=args['data'])
            # db.collection('packages').document(package.metadata['Name'] + '_' + package.metadata['Version']).set(package.to_dict())
            # Check to see if package already exists
            packages_ref = db.collection('packages')
            docs = packages_ref.stream()
            package.metadata['ID'] = package.metadata['ID'] + '_' + package.metadata['Version']
            for doc in docs:
                if doc.to_dict()['metadata']['ID'] == package.metadata['ID']:
                    return 'Package already exists', 403
            if ("Content" in package.to_dict()['data']):
                db.collection('packages').document(package.metadata['ID']).set(package.to_dict())
                return package.to_dict()['metadata'], 201
            else:
                URL = package.data['URL']
                if isIngestible(URL):
                    db.collection('packages').document(package.metadata['ID']).set(package.to_dict())
                    return package.to_dict()['metadata'], 201
            return 'URL not ingestible', 400
        except: return 'Malformed request', 400

    # Get package by ID
    @app.route("/package/<packageid>", methods = ['GET'])
    def retrievePackage(packageid):
        try:
            packages_ref = db.collection('packages')
            docs = packages_ref.stream()
            for doc in docs:
                if doc.to_dict()['metadata']['ID'] == packageid:
                    return doc.to_dict(), 200
            return jsonify(code=0, message="Package with ID '" + packageid + "' not found")
        except: return jsonify(code=0, message="An error occurred while retrieving package")
    
    # Get package by name
    @app.route("/package/byName/<name>", methods = ['GET'])
    def retrievePackageByName(name):
        try:
            packages_ref = db.collection('packages')
            docs = packages_ref.stream()
            packages = []
            foundFlag = 0
            for doc in docs:
                if doc.to_dict()['metadata']['Name'] == name:
                    foundFlag = 1
                    packages.append(doc.to_dict()['metadata'])
            if foundFlag:
                return jsonify(packages), 200
            return jsonify(code=0, message="Package with name '" + name + "' not found")
        except: return jsonify(code=0, message="An error occurred while retrieving package")

    # Update package
    @app.route("/package/<packageid>", methods = ['PUT'])
    def updatePackage(packageid):
        try:
            args = parser.parse_args()
            package = Package(metadata=args['metadata'], data=args['data'])
            packages_ref = db.collection('packages')
            docs = packages_ref.stream()
            # db.collection('packages').document().update({"data": args['data'], "metadata": args['metadata']})
            for doc in docs:
                print(doc.to_dict()['metadata']['ID'])
                print(packageid)
                if doc.to_dict()['metadata']['ID'] == packageid:
                    docID = doc.to_dict()['metadata']['ID']
                    db.collection('packages').document(docID).update({"data": args['data'], "metadata": args['metadata']})
                    return args, 200
            print('Could not find requested version of ' + packageid)
            return 'Could not find requested version of ' + packageid, 400
        except: return 'Malformed request', 400
    
    # Request audit
    @app.route("/package/<packageid>/audit", methods = ['GET'])
    def auditPackage(packageid):
        packages_ref = db.collection('packages')
        docs = packages_ref.stream()
        try:
            for doc in docs:
                if doc.to_dict()['metadata']['ID'] == packageid:
                    utilities.strToZip(doc.to_dict()['data']['Content'], 'tmp/' + packageid + '.zip')
                    output = utilities.auditPackage('tmp/' + packageid + '.zip')
                    return output[0], 200
            return jsonify(code=0, message="Package with ID '" + packageid + "' not found"), 400
        except: return jsonify(code=0, message="An error occurred while retrieving package"), 500

    # Delete package by ID
    @app.route("/package/<packageid>", methods = ['DELETE'])
    def deletePackage(packageid):
        try:
            packages_ref = db.collection('packages')
            docs = packages_ref.stream()
            for doc in docs:
                if doc.to_dict()['metadata']['ID'] == packageid:
                    docID = doc.to_dict()['metadata']['ID']
                    db.collection('packages').document(docID).delete()
                    return '', 200
            return '', 400
        except: return '', 400
    
    # Delete all versions of package
    @app.route("/package/byName/<packageName>", methods = ['DELETE'])
    def deletePackageByName(packageName):
        try:
            packages_ref = db.collection('packages')
            docs = packages_ref.stream()
            foundFlag = 0
            for doc in docs:
                if doc.to_dict()['metadata']['Name'] == packageName:
                    foundFlag = 1
                    docID = doc.to_dict()['metadata']['ID']
                    db.collection('packages').document(docID).delete()
            if foundFlag:
                return '', 200
            else:
                return '', 400
        except: return '', 400

    # Reset registry
    @app.route("/reset", methods = ['DELETE'])
    def resetRegistry():
        try:
            packages_ref = db.collection('packages')
            docs = packages_ref.stream()
            for doc in docs:
                docID = doc.to_dict()['metadata']['ID']
                db.collection('packages').document(docID).delete()
                print("deleted " + docID)
            return '', 200
        except: return '', 401

    # Rate package by ID
    @app.route("/package/<packageid>/rate", methods = ['GET'])
    def ratePackage(packageid):
        try:
            packages_ref = db.collection('packages')
            docs = packages_ref.stream()
            for doc in docs:
                if doc.to_dict()['metadata']['ID'] == packageid:
                    docID = doc.to_dict()['metadata']['ID']
                    # if no score for one of the metrics:
                    #     return '', 500
                    # else:
                    URL = doc.to_dict()['data']['URL']
                    scores = rate(URL)
                    # print(scores)
                    return jsonify(RampUp = scores[1], Correctness = scores[2], BusFactor = scores[3], ResponsiveMaintainer = scores[4], LicenseScore = scores[5], GoodPinningPractice = scores[6]), 200
                    # return '', 200
            print('Could not find ' + packageid)
            return '', 400
        except: return 'Error calculating metrics', 500

    @app.route('/authenticate', methods = ['PUT'])
    def create_token():
        try:
            args = parser.parse_args()
            # auth = request.authorization

            if args['Secret']['password'] == 'correcthorsebatterystaple123(!__+@**(A':
                token = jwt.encode({'user' : args['User']['name'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=10)}, app.config['SECRET_KEY'])
                return token.decode('UTF-8'), 200

            return 'no such user or invalid password', 401
        except: return 'This system does not support authentication', 501

    
    # Register and Login user
    # @app.route("/auth/user", methods=["POST"])
    # def register():
    #     user_data = request.get_json()
    #     try:
    #         user = UserModel(**user_data)
    #         user.create_user()
    #         token: str = jwt_routes.register_entity(entity_id=user.id, entity_type="users")
    #         return jsonify(message="User successfully created", token=str(token)), 200
    #     except:
    #         return jsonify(message="Error creating user"), 500
    
    # @app.route("/auth/user", methods=["GET"])
    # def login():
    #     if "users" not in g:
    #         return '', 404
    #     try:
    #         teacher_dumped = UserSchema().dump(g.teachers)
    #         return jsonify(data=teacher_dumped, token=jwt_routes.update_entity(entity_id=g.teachers.teacher_id)), 200
    #     except ValidationError as _:
    #         return '', 404

    def __repr__(self):
        return 'Package(medatada={}, data={})'.format(self.medadata, self.data)
    

parser = reqparse.RequestParser()
parser.add_argument('metadata', type=dict)
parser.add_argument('data', type=dict)

api.add_resource(PackageList, '/packages', '/package', '/package/<packageid>', '/reset', '/package/<packageid>/rate', '/authenticate') # '/auth/user')

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World! I can update automatically now! CHANGEEEEEE'


def isIngestible(URL):
    scores = rate(URL)
    print(scores)
    if (all(float(i) >= 0.5 for i in scores)):
        print("Ingestible")
        return True
    else:
        print("Not Ingestible")
        return False


def rate(URL): 
    with open("/tmp/URL.txt", "w") as f:
        f.write(URL)
    scores = p1.Run.scoreRepos("/tmp/URL.txt")
    return scores

    # print(scores)
    



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    # rate() 
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
