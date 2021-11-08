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
from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from google.cloud import firestore

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
        return 'Package(medatada={}, data={}, priority={})'.format(self.medadata, self.data)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
db = firestore.Client()
api = Api(app)



class PackageList(Resource):
    def get(self):
        packages_ref = db.collection('Packages')
        docs = packages_ref.stream()
        packages = {}
        for doc in docs:
            packages[doc.id]= doc.to_dict()
        return packages

    def post(self):
        args = parser.parse_args()
        package = Package(metadata=args['metadata'], data=args['data'])
        db.collection('Packages').document(package.metadata['Name'] + '_' + package.metadata['Version']).set(package.to_dict())
        return package.to_dict(), 201

    def __repr__(self):
        return 'Package(medatada={}, data={}, priority={})'.format(self.medadata, self.data)

parser = reqparse.RequestParser()
parser.add_argument('metadata', type=dict)
parser.add_argument('data', type=dict)

api.add_resource(PackageList, '/Packages')

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
