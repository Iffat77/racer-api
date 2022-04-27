from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from playhouse.postgres_ext import ArrayField

import os

from playhouse.db_url import connect

DATABASE = connect(os.environ.get('https://git.heroku.com/racerp9.git'))


# DATABASE = PostgresqlDatabase('teams', user='iffathossain',
#                         password='', host='localhost', port=5432)

# DATABASE.connect()


class BaseModel(Model):
    class Meta:
        database = DATABASE


class Team(BaseModel):
    name = CharField()
    drivers = ArrayField(CharField)
    wins = IntegerField()
    country_id = IntegerField()

class Country(BaseModel):
    name = CharField()
    tracks = ArrayField(CharField)


DATABASE.drop_tables([Team])
DATABASE.create_tables([Team])


Team(name='Ferrari', drivers=['Charles', 'Carlos'], wins=2, country_id=5).save()
Team(name='Mercedes', drivers=['Lewis', 'George'], wins=0, country_id=1).save()
Team(name='Red Bull', drivers=['Max', 'Sergio'], wins=2, country_id=1).save()
Team(name='Mclaren', drivers=['Lando', 'Ricciardo'], wins=0, country_id=1).save()
Team(name='Alpha Tauri', drivers=['Yuki', 'Pierre'], wins=0, country_id=5).save()
Team(name='Alpine', drivers=['Fernando', 'Estaban'], wins=0, country_id=3).save()
Team(name='Haas', drivers=['Mick', 'Kevin'], wins=0, country_id=2).save()
Team(name='Williams', drivers=['Nicholas', 'Alex'], wins=0, country_id=1).save()
Team(name='Alfa Romeo', drivers=['Valtteri', 'Zhou'], wins=0, country_id=5).save()
Team(name='Aston Martin', drivers=['Sebastian', 'Lance'], wins=0, country_id=1).save()

DATABASE.create_tables([Country])
DATABASE.drop_tables([Country])
DATABASE.create_tables([Country])
Country(name="United Kingdom", tracks=['Silvetstone']).save()
Country(name="United States", tracks=["COTA", "Miami gp"]).save()
Country(name="France", tracks=["Circuit Paul Ricard"]).save()
Country(name="Japan", tracks=["Suzuka Circuit"]).save()
Country(name="Italy", tracks=["Imola", "Monza"]).save()

# Initialize Flask
# We'll use the pre-defined global '__name__' variable to tell Flask where it is.


if 'ON_HEROKU' in os.environ:
    print('hitting ')
    Team.initialize()
    Country.initialize()


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

    # if request.method == 'GET':
    #   if id:
    #    teams = Team.select().where(Team.country_id == id).execute()
    #    jointeam = []
    #    for team in teams:
    #        jointeam.append(model_to_dict(team))
    #    country = model_to_dict(Country.get_by_id(id))

    #    return jsonify({'country': country, 'team': jointeam})
    # else:
    #   country_list = []
    #   for unit in Country.select():
    #     country_list.append(model_to_dict(unit))
    #   return jsonify(country_list)




@app.route('/countries/', methods=['GET', 'POST'])
@app.route('/country/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpointer(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Country.get(Country.id == id)))
        else:
            countryList = []
            for country in Country.select():
                countryList.append(model_to_dict(country))
            return jsonify(countryList)

    if request.method == 'PUT':
        country_up = request.get_json()
        Country.update(country_up).where(Country.id == id).execute()
        return ("updated")

    if request.method == 'POST':
        new_country = dict_to_model(Country, request.get_json())
        new_country.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        team = Country.get(Country.id == id)
        team.delete_instance()
        return 'Deleted'

if __name__ == '__main__':
  app.run(debug=True, port=5000)

