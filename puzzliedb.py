from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
from datetime import datetime
from flask_cors import CORS
from urllib.parse import unquote_plus

app = Flask(__name__, static_url_path='')
CORS(app)

db_name = 'puzzlie_team_tms'
client = None
db = None


# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


user = "d1565c63-813c-4353-9b50-692e032865fc-bluemix"
password = "7b6ae87a8beef28a836d1407ecbf4043c2d69d6746a231c551302d1f94f75255"
url = 'https://' + "d1565c63-813c-4353-9b50-692e032865fc-bluemix.cloudantnosqldb.appdomain.cloud"
client = Cloudant(user, password, url=url, connect=True)
db = client.create_database(db_name, throw_on_exists=False)

@app.route('/register', methods=['GET'])
def register():
    id = unquote_plus(request.args['name'])
    password = unquote_plus(request.args['password'])
    email1 =unquote_plus(request.args['email1'])
    email2 =unquote_plus(request.args['email2'])
    email3 =unquote_plus(request.args['email3'])
    email4 =unquote_plus(request.args['email4'])
    email5 =unquote_plus(request.args['email5'])
    if (email1 == 'undefined'):
        email1 = ''
    if (email2 == 'undefined'):
        email2 = ''
    if (email3 == 'undefined'):
        email3 = ''
    if (email4 == 'undefined'):
        email4 = ''
    if (email5 == 'undefined'):
        email5 = ''

    teams = list(map(lambda doc: doc, db))
    for team in teams:
        if (team["_id"].lower() == id.lower()):
            return 'Team ' + id + ' exists'
        elif (email1.lower() != '' and (email1.lower() == team["email1"].lower() or email1.lower() == team["email2"].lower() or email1.lower() == team["email3"].lower() or email1.lower() == team["email4"].lower() or email1.lower() == team["email5"].lower() )):
            return 'Email ' + email1 + ' is already registered'
        elif (email2.lower() != '' and (email2.lower() == team["email1"].lower() or email2.lower() == team["email2"].lower() or email2.lower() == team["email3"].lower() or email2.lower() == team["email4"].lower() or email2.lower() == team["email5"].lower() )):
            return 'Email ' + email2 + ' is already registered'
        elif (email3.lower() != '' and (email3.lower() == team["email1"].lower() or email3.lower() == team["email2"].lower() or email3.lower() == team["email3"].lower() or email3.lower() == team["email4"].lower() or email3.lower() == team["email5"].lower() )):
            return 'Email ' + email3 + ' already registered'
        elif (email4.lower() != '' and (email4.lower() == team["email1"].lower() or email4.lower() == team["email2"].lower() or email4.lower() == team["email3"].lower() or email4.lower() == team["email4"].lower() or email4.lower() == team["email5"].lower() )):
            return 'Email ' + email4 + ' already registered'
        elif (email5.lower() != '' and (email5.lower() == team["email1"].lower() or email5.lower() == team["email2"].lower() or email5.lower() == team["email3"].lower() or email5.lower() == team["email4"].lower() or email5.lower() == team["email5"].lower() )):
            return 'Email ' + email5 + ' already registered'

    data = {'_id':id,
            'password':password,
            'email1':email1,
            'email2':email2,
            'email3':email3,
            'email4':email4,
            'email5':email5,
            'current':'level1',
            'timestamp': datetime.now().strftime("%b %d %Y %H:%M:%S"),
            'sort': 0,
            'completed':''}
    if client:
        doc = db.create_document(data)
        data['_id'] = doc['_id']

    return 'Team ' + id + ' registered'


@app.route('/login', methods=['GET'])
def login():
    id = unquote_plus(request.args['name'])
    password = unquote_plus(request.args['password'])
    teams = list(map(lambda doc: doc, db))
    for team in teams:
        if (team["_id"] == id and team["password"] == password):
            return team["current"]

    return 'false'



@app.route('/current', methods=['GET'])
def current():
    id = unquote_plus(request.args['name'])
    doc = db[id]
    return doc['current']

@app.route('/completed', methods=['GET'])
def completed():
    id = request.args['name']
    doc = db[id]
    return doc['completed']


@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    teams = list(map(lambda doc: {'name': doc['_id'], 'current': doc['current'], 'timestamp': doc['timestamp'], 'sort': doc['sort']}, db))
    for team in teams:
        if (team["current"] == "user"):
            team["current"] = "All Done!"
    teams.sort(key = lambda l: (l['sort'] * -1, l['timestamp']))
    return jsonify(teams)


@app.route('/update', methods=['GET'])
def update():
    id = unquote_plus(request.args['name'])
    level = request.args['level']
    answer = request.args['answer']
    data = {level: datetime.now().strftime("%b %d %Y %H:%M:%S")}
    completed = {'completed': level}
    currentTime = {'timestamp': datetime.now().strftime("%b %d %Y %H:%M:%S")}
    doc = db[id]
    doc.update(data)
    doc.update(completed)
    doc.update(currentTime)
    if (level == 'level1' and answer.lower() == 'arvind krishna'):
        current = {'current': 'level2'}
        doc.update(current)
        doc.update({'sort': 1})
        doc.save()
        return 'true'
    if (level == 'level2' and (answer.lower() == 'bluepages' or answer.lower() == 'blue pages')  and ('level1' in str(doc)) ):
        current = {'current': 'level3'}
        doc.update(current)
        doc.update({'sort': 2})
        doc.save()
        return 'true'
    if (level == 'level3' and answer.lower() == 'gbs'  and ('level2' in str(doc))  ):
        current = {'current': 'level4'}
        doc.update(current)
        doc.update({'sort': 3})
        doc.save()
        return 'true'
    if (level == 'level4' and (answer.lower() == 'block chain' or answer.lower() == 'blockchain') and ('level3' in str(doc)) ):
        current = {'current': 'level5'}
        doc.update(current)
        doc.update({'sort': 4})
        doc.save()
        return 'true'
    if (level == 'level5' and (answer.lower() == 'kitne aadmi the' or answer.lower() == 'kitney aadmi the'
                                 or answer.lower() == 'kitne aadmi they' or answer.lower() == 'kitne aadmi thay') and ('level4' in str(doc)) ):
        current = {'current': 'level6'}
        doc.update(current)
        doc.update({'sort': 5})
        doc.save()
        return 'true'
    if (level == 'level6' and (answer.lower() == 'lighthouse') and ('level5' in str(doc))  ):
        current = {'current': 'level7'}
        doc.update(current)
        doc.update({'sort': 6})
        doc.save()
        return 'true'
    if (level == 'level7' and (answer.lower() == 'curfew') and ('level6' in str(doc))  ):
        current = {'current': 'level8'}
        doc.update(current)
        doc.update({'sort': 7})
        doc.save()
        return 'true'
    if (level == 'level8' and (answer.lower() == 'hidden figures') and ('level7' in str(doc))  ):
        current = {'current': 'level9'}
        doc.update(current)
        doc.update({'sort': 8})
        doc.save()
        return 'true'
    if (level == 'level9' and (answer.lower() == 'covid-19' or answer.lower() == 'covid 19' or answer.lower() == 'covid19') and ('level8' in str(doc)) ):
        current = {'current': 'level10'}
        doc.update(current)
        doc.update({'sort': 9})
        doc.save()
        return 'true'
    if (level == 'level10' and (answer.lower() == 'william shakespeare') and ('level9' in str(doc)) ):
        current = {'current': 'level11'}
        doc.update(current)
        doc.update({'sort': 10})
        doc.save()
        return 'true'
    if (level == 'level11' and (answer.lower() == 'microsoft') and ('level10' in str(doc)) ):
        current = {'current': 'level12'}
        doc.update(current)
        doc.update({'sort': 11})
        doc.save()
        return 'true'
    if (level == 'level12' and (answer.lower() == 'in kutton ke samne mat nachna') and ('level11' in str(doc)) ):
        current = {'current': 'level13'}
        doc.update(current)
        doc.update({'sort': 12})
        doc.save()
        return 'true'
    if (level == 'level13' and (answer.lower() == 'bill gates') and ('level12' in str(doc)) ):
        current = {'current': 'level14'}
        doc.update(current)
        doc.update({'sort': 13})
        doc.save()
        return 'true'
    if (level == 'level14' and (answer.lower() == 'sherlock holmes' or answer.lower() == 'sherlock homes') and ('level13' in str(doc)) ):
        current = {'current': 'level15'}
        doc.update(current)
        doc.update({'sort': 14})
        doc.save()
        return 'true'
    if (level == 'level15' and (answer.lower() == 'lamborghini' or answer.lower() == 'lamborgini') and ('level14' in str(doc)) ):
        current = {'current': 'user'}
        doc.update(current)
        doc.update({'sort': 15})
        doc.save()
        return 'true'
    else:
        return 'false'



@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
