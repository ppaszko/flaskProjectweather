import json
import pandas as pd
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from visuals2 import draw_ceiling_clouds, mydraw



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
    data=data.drop_duplicates(subset="datetime:",
                         keep='first')
    data.index = pd.to_datetime(data['datetime:'], )
    weather_data = data
    image_name = draw_ceiling_clouds(weather_data, None)
    custom_plot1 = 'static/images/fig21.png'
    print('kuźwa')
    selected_weather = weather_data.iloc[-1]

    return render_template('weather.html', weather_data=selected_weather, ceiling_image=image_name,
                           custom_plot1=custom_plot1)



@app.route('/', methods=['GET', 'POST'])
def index():

    with open('/home/paszko/PycharmProjects/flaskProject/epkt.json') as f:
        data = pd.DataFrame(json.load(f)['airport_info'])
    data=data.drop_duplicates(subset="datetime:",
                         keep='first')
    data.index = pd.to_datetime(data['datetime:'], )
    weather_data = data
    image_name = draw_ceiling_clouds(weather_data, None)
    custom_plot1 = 'static/images/fig21.png'
    selected_weather = weather_data.iloc[-1]

    if request.method == 'POST':

        if 'airport' in request.form:
            hehe = request.form['airport']
            if request.form['day'] != '':
                day =request.form['day']
                time=request.form['time']
                time = str(day) + 'T' + str(time) + ':00.000Z'
                print(time)
            else:
                time=None
            print('lujjj')

            with open('/home/paszko/PycharmProjects/flaskProject/'+ str(hehe) + '.json') as f:
                data = pd.DataFrame(json.load(f)['airport_info'])
            data=data.drop_duplicates(subset="datetime:",
                                 keep='first')
            data.index = pd.to_datetime(data['datetime:'], )
            weather_data = data
            if time:
                # time = pd.to_datetime(time)
                # print(pd.Index(data_ceiling['datetime:']))
                luj = pd.Index(weather_data['datetime:']).get_loc(time)
                # print(luj)
            else:
                luj = -1

            selected_weather=weather_data.iloc[luj]
            print(selected_weather)
            image_name = draw_ceiling_clouds(weather_data, time)

        if 'day1' in request.form:
            hehe = request.form['airport2']
            with open('/home/paszko/PycharmProjects/flaskProject/'+ str(hehe) + '.json') as f:
                data = pd.DataFrame(json.load(f)['airport_info'])
            data=data.drop_duplicates(subset="datetime:",
                                 keep='first')
            data.index = pd.to_datetime(data['datetime:'], )
            weather_data = data
            image_name = draw_ceiling_clouds(weather_data, None)
            day1=request.form['day1']
            time1_start=request.form['time1_start']
            time1_end = request.form['time1_end']
            parameter1=request.form['parameter1']
            start1 = str(day1) + 'T' + str(time1_start) + ':00.000Z'
            end1 = str(day1) + 'T' + str(time1_end) + ':00.000Z'
            custom_plot1 = mydraw(weather_data,parameter1,start1,end1)



    return render_template('weather.html', weather_data=selected_weather, ceiling_image=image_name, custom_plot1=custom_plot1)


"""        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()"""

# cities = City.query.all()

# url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
# url ='https://danepubliczne.imgw.pl/api/data/synop/station/krakow'