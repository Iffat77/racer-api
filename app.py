from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from playhouse.postgres_ext import ArrayField

db = PostgresqlDatabase('teams', user='iffathossain',
                        password='', host='localhost', port=5432)

db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Team(BaseModel):
    name = CharField()
    drivers = ArrayField(CharField)
    wins = IntegerField()


db.drop_tables([Team])
db.create_tables([Team])

Team(name='Ferrari', drivers=['Charles', 'Carlos'], wins=2).save()
Team(name='Mercedes', drivers=['Lewis', 'George'], wins=0).save()
Team(name='Red Bull', drivers=['Max', 'Sergio'], wins=2).save()
Team(name='Aston Martin', drivers=['Sebastian', 'Lance'], wins=0).save()


# Initialize Flask
# We'll use the pre-defined global '__name__' variable to tell Flask where it is.
app = Flask(__name__)


@app.route('/teams/', methods=['GET', 'POST'])
@app.route('/teams/<id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/drivers/<driver>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None, driver=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Team.get(Team.id == id)))
        elif driver:
            all_teams = Team.select()
            for team in all_teams:
                if driver in team.drivers:
                    return jsonify(model_to_dict(team))
        else:
            teamList = []
            for team in Team.select():
                teamList.append(model_to_dict(team))
            return jsonify(teamList)

    if request.method == 'PUT':
        team_up = request.get_json()
        Team.update(team_up).where(Team.id == id).execute()
        return ("updated")

    if request.method == 'POST':
        new_team = dict_to_model(Team, request.get_json())
        new_team.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        team = Team.get(Team.id == id)
        team.delete_instance()
        return 'Deleted'


app.run(debug=True, port=9100)

