from flask import Flask, request, jsonify #modules #flask-parent(back end) #Flask-child #request:module handle client sent request,json:thunder client understands,converts into doc obj to json
from flask_cors import CORS#cors-cross origin resource service  #used for security purpose #flask is the framework which handles the request(end to end),microweb server
from mongoengine import connect, Document, StringField
from bson import ObjectId

app = Flask(__name__) #app: flask obj 
CORS(app)  #assign app to cors-rejects all other requests other than app# Enable CORS for all routes

# Connect to MongoDB
connect('person_db', host='localhost', port=27017)# connects to mongo

class Person(Document):#module is created with rules
    name = StringField(required=True, max_length=100)
    gender = StringField(required=True, choices=['Male', 'Female', 'Other'])
    location = StringField(required=True, max_length=200)

# Create a Person
@app.route('/person', methods=['POST'])#/person is home page,post-insert record into page, 
def add_person():
    data = request.json#request from client contains person details,data is json obj,doc is python object
    person = Person(           #py obj
        name=data['name'],        #datatype=defined object from 12,13,14
        gender=data['gender'],
        location=data['location']
    )
    person.save()#connects to mongodbinsert command run and save
    return jsonify({'message': 'Person added successfully', 'id': str(person.id)}), 201 #rerurn the client,jsonify converts the person id into string and json and returns

# Get all Persons,get-read from the collection
@app.route('/person', methods=['GET'])
def get_all_persons():
    persons = Person.objects()# reads all the objects
    person_list = [{**person.to_mongo().to_dict(), '_id': str(person.id)} for person in persons]#[]-is list,id to str,else is to dict
    return jsonify(person_list), 200#200 is status,success

# Get a Person by ID
@app.route('/person/<string:person_id>', methods=['GET'])#get-read,id is converted to string,client needs id
def get_person(person_id):
    person = Person.objects(id=ObjectId(person_id)).first()#selects a particular id
    if person: #if means-got, if not-not got
        person_data = person.to_mongo().to_dict()
        person_data['_id'] = str(person.id)#id-crucial data
        return jsonify(person_data), 200#client-json,py-dict,mongo-doc,200-status,success
    return jsonify({'error': 'Person not found'}), 404#404-status,error

# Update a Person
@app.route('/person/<string:person_id>', methods=['PUT'])#put-update
def update_person(person_id):
    data = request.json
    person = Person.objects(id=ObjectId(person_id)).first()
    if person:
        person.update(**data)#json convert to python to 
        return jsonify({'message': 'Person updated successfully'}), 200#name,gender etc is converted to json for updation
    return jsonify({'error': 'Person not found'}), 404

# Delete a Person
@app.route('/person/<string:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = Person.objects(id=ObjectId(person_id)).first()
    if person:
        person.delete()
        return jsonify({'message': 'Person deleted successfully'}), 200
    return jsonify({'error': 'Person not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)