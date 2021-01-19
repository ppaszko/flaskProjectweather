import pandas as pd
import json
from visualization import draw_ceiling_clouds


def json_default():
    """Function using in first load of airport.html."""
    weather_data = data_load('epkt')
    image_name = draw_ceiling_clouds(weather_data, None)
    custom_plot1 = 'static/images/default_horizontal.png'
    selected_weather = weather_data.iloc[-1]
    datetime_formated = selected_weather['datetime:']
    datetime_output = datetime_formated[0:10] + ' ' + datetime_formated[11:16]

    return selected_weather, image_name, custom_plot1, datetime_output


def data_load(icao_code):
    """Load data from .json file and preprocess."""
    with open('/home/paszko/PycharmProjects/flaskProject/' + str(icao_code) + '.json') as f:
        data = pd.DataFrame(json.load(f)['airport_info'])
    data = data.drop_duplicates(subset="datetime:", keep='first')
    data.index = pd.to_datetime(data['datetime:'], )
    weather_data = data
    return weather_data
