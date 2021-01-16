import json
from datetime import timezone

import pandas as pd
import pytz
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from visuals import draw_wth_trend
from visuals2 import draw_ceiling_clouds, mydraw
import datetime
import pytz



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)



flag=False

@app.route('/')
def home():
    with open('/home/paszko/PycharmProjects/flaskProject/epkt.json') as f:
        data = pd.DataFrame(json.load(f)['airport_info'])
    data.drop_duplicates(subset="datetime:",
                         keep='first')
    data.index = pd.to_datetime(data['datetime:'], )
    weather_data = data
    image_name = draw_ceiling_clouds(weather_data)
    custom_plot1 = 'static/images/fig21.png'
    print('kuźwa')
    return render_template('weather.html', weather_data=weather_data, ceiling_image=image_name,
                           custom_plot1=custom_plot1)


@app.route('/', methods=['GET', 'POST'])
def index():

    with open('/home/paszko/PycharmProjects/flaskProject/epkt.json') as f:
        data = pd.DataFrame(json.load(f)['airport_info'])
    data.drop_duplicates(subset="datetime:",
                         keep='first')
    data.index = pd.to_datetime(data['datetime:'], )
    weather_data = data
    image_name = draw_ceiling_clouds(weather_data)
    custom_plot1 = 'static/images/fig21.png'

    if request.method == 'POST':
        if 'airport' in request.form:
            hehe = request.form['airport']
            print('lujjj')
            with open('/home/paszko/PycharmProjects/flaskProject/'+ str(hehe) + '.json') as f:
                data = pd.DataFrame(json.load(f)['airport_info'])
            data.drop_duplicates(subset="datetime:",
                                 keep='first')
            data.index = pd.to_datetime(data['datetime:'], )
            weather_data = data
            image_name = draw_ceiling_clouds(weather_data)

        if 'day1' in request.form:
            hehe = request.form['airport2']
            with open('/home/paszko/PycharmProjects/flaskProject/'+ str(hehe) + '.json') as f:
                data = pd.DataFrame(json.load(f)['airport_info'])
            data.drop_duplicates(subset="datetime:",
                                 keep='first')
            data.index = pd.to_datetime(data['datetime:'], )
            weather_data = data
            image_name = draw_ceiling_clouds(weather_data)
            day1=request.form['day1']
            time1_start=request.form['time1_start']
            time1_end = request.form['time1_end']
            parameter1=request.form['parameter1']
            start1 = str(day1) + 'T' + str(time1_start) + ':00.000Z'
            end1 = str(day1) + 'T' + str(time1_end) + ':00.000Z'
            custom_plot1 = mydraw(weather_data,parameter1,start1,end1)
            #timezone.utc()
            #print(datetime1)
            #print(weather_data[weather_data['datetime:'] == datetime1][parameter1])

        if 'day2' in request.form:
            day2 = request.form['day2']
            time2_start=request.form['time2_start']
            time2_end = request.form['time2_end']
            parameter2 = request.form['parameter2']


    return render_template('weather.html', weather_data=weather_data, ceiling_image=image_name, custom_plot1=custom_plot1)


"""        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()"""

# cities = City.query.all()

# url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
# url ='https://danepubliczne.imgw.pl/api/data/synop/station/krakow'