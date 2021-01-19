import json
import pandas as pd
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from utils import json_default, data_load
from visualization import draw_ceiling_clouds, mydraw
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

class Airport(db.Model):
    """Database Airport class"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

@app.route('/')
def home():
    """First run of airports.html."""
    selected_weather, image_name, custom_plot1, datetime_output = json_default()
    airports = [T.name for T in Airport.query.all()]
    print(airports)
    return render_template('airports.html', weather_data=selected_weather, ceiling_image=image_name,
                           custom_plot1=custom_plot1, datetime_output=datetime_output, airports=airports)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main usage of airports.html"""
    selected_weather, image_name, custom_plot1, datetime_output = json_default()
    airports = [T.name for T in Airport.query.all()]

    if request.method == 'POST':
        new_airport = request.form.get('new_airport')
        if new_airport:
            """New airport procedure"""
            new_city_obj = Airport(name=new_airport)
            db.session.add(new_city_obj)
            db.session.commit()
            airports = [T.name for T in Airport.query.all()]
            with open('default.json', 'r') as f:
                data = json.load(f)
            with open(str(new_airport) + '.json', 'w') as file:
                json.dump(data, file, indent=4)
            from requester import all_request
            all_request()

        if 'airport' in request.form:
            """Upper input fields"""
            icao_code = request.form['airport']
            if request.form['day'] != '':
                day = request.form['day']
                time = request.form['time']
                time = str(day) + 'T' + str(time) + ':00.000Z'
            else:
                time = None
            weather_data = data_load(icao_code)
            if time:
                luj = pd.Index(weather_data['datetime:']).get_loc(time)
            else:
                luj = -1
            selected_weather = weather_data.iloc[luj]
            datetime_formated = selected_weather['datetime:']
            datetime_output = datetime_formated[0:10] + ' ' + datetime_formated[11:16]
            image_name = draw_ceiling_clouds(weather_data, time)

        if 'day1' in request.form:
            """Bottom input fields"""
            icao_code = request.form['airport2']
            weather_data = data_load(icao_code)
            if request.form['day1'] != '':
                day = request.form['day1']
                time = request.form['time1_end']
                time = str(day) + 'T' + str(time) + ':00.000Z'
            else:
                time = None
            if time:
                luj = pd.Index(weather_data['datetime:']).get_loc(time)
            else:
                luj = -1
            day1 = request.form['day1']
            time1_start = request.form['time1_start']
            time1_end = request.form['time1_end']
            parameter1 = request.form['parameter1']
            selected_weather = weather_data.iloc[luj]
            datetime_formated = selected_weather['datetime:']
            datetime_output = datetime_formated[0:10] + ' ' + datetime_formated[11:16]
            start1 = str(day1) + 'T' + str(time1_start) + ':00.000Z'
            end1 = str(day1) + 'T' + str(time1_end) + ':00.000Z'
            custom_plot1 = mydraw(weather_data, parameter1, start1, end1)

    return render_template('airports.html', weather_data=selected_weather, ceiling_image=image_name,
                           custom_plot1=custom_plot1, datetime_output=datetime_output, airports=airports)
