
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,  jsonify, request
# import os
import boto3
import io
# import csv


AWS_SECRET_KEY_ID = "AKIA33SE4OYZHEPBTIOK"
AWS_SECRET_KEY = "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"

session = boto3.Session(aws_access_key_id = AWS_SECRET_KEY_ID, aws_secret_access_key=AWS_SECRET_KEY)

#Then use the session to get the resource
s3 = session.resource('s3')

my_bucket = s3.Bucket('pruebapythonanywhere')

app = Flask(__name__)

@app.route('/')
def hello_world():

    return "hola"

@app.route('/get_object/<string:id>')
def get_object(id):
    obj = s3.Object('pruebapythonanywhere', id)
    data = io.BytesIO()
    obj.download_fileobj(data)

    # object is now a bytes string, Converting it to a dict:
    response = data.getvalue().decode("utf-8")

    return response

@app.route('/put_object', methods=['POST'])
def put_object():
    data = request.json
    csv_data = data["csv"]
    fo = io.BytesIO(bytes(csv_data, 'utf-8'))
    my_bucket.upload_fileobj(fo, data["name"])

    return 'put_object'

@app.route('/remove_object/<string:id>')
def remove_object(id):
    s3.Object('pruebapythonanywhere', id).delete()
    return "Success"


@app.route('/list_objects')
def list_objects():
    res = []
    for obj in my_bucket.objects.all():
        if obj.key.endswith('csv'):
            res.append(obj.key)
    return jsonify({"res":res})


