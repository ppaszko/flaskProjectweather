import time

import requests
import json
import os
import requester
import schedule

def job():
    airports=['epkt', 'epkk', 'epwa', 'epwr', 'epgd', 'eprz', 'eppo']


    def request(airport):
        hdr = {"X-API-Key": "78beb76cf00149519431af799e"}
        req = requests.get('https://api.checkwx.com/metar/'+ str(airport)+'/decoded', headers=hdr)

        try:
            req.raise_for_status()
            resp = json.loads(req.text)
            print(resp)
            try:
                weather={
                    'airport:': resp["data"][0]["station"]["name"],
                    'category:': resp["data"][0]["flight_category"],
                    'conditions:': resp["data"][0]["conditions"][0]["text"],
                    'datetime:': resp["data"][0]["observed"],
                    'temperature:': resp["data"][0]["temperature"]["celsius"],
                    'wind_degrees:': resp["data"][0]["wind"]["degrees"],
                    'wind_speed:': resp["data"][0]["wind"]["speed_kph"],
                    'dewpoint:': resp["data"][0]["dewpoint"]["celsius"],
                    'humidity:': resp["data"][0]["humidity"]["percent"],
                    'pressure:': resp["data"][0]["barometer"]["hpa"],
                    'visibility:': resp["data"][0]["visibility"]["meters_float"],
                    'ceiling:': resp["data"][0]["ceiling"]["text"],
                    'ceiling_level:': resp["data"][0]["ceiling"]["meters"],
                    'clouds1:': resp["data"][0]["clouds"][0]["text"],
                    'clouds1_level:': resp["data"][0]["clouds"][0]["meters"],
                }
            except (KeyError,IndexError) as e:
                try:
                    weather = {
                        'airport:': resp["data"][0]["station"]["name"],
                        'category:': resp["data"][0]["flight_category"],
                        'datetime:': resp["data"][0]["observed"],
                        'temperature:': resp["data"][0]["temperature"]["celsius"],
                        'wind_degrees:': resp["data"][0]["wind"]["degrees"],
                        'wind_speed:': resp["data"][0]["wind"]["speed_kph"],
                        'dewpoint:': resp["data"][0]["dewpoint"]["celsius"],
                        'humidity:': resp["data"][0]["humidity"]["percent"],
                        'pressure:': resp["data"][0]["barometer"]["hpa"],
                        'visibility:': resp["data"][0]["visibility"]["meters_float"],
                        'ceiling:': resp["data"][0]["ceiling"]["text"],
                        'ceiling_level:': resp["data"][0]["ceiling"]["meters"],
                        'clouds1:': resp["data"][0]["clouds"][0]["text"],
                        'clouds1_level:': resp["data"][0]["clouds"][0]["meters"],
                    }
                except (KeyError,IndexError) as e:
                    try:
                        weather = {
                            'airport:': resp["data"][0]["station"]["name"],
                            'category:': resp["data"][0]["flight_category"],
                            'datetime:': resp["data"][0]["observed"],
                            'temperature:': resp["data"][0]["temperature"]["celsius"],
                            'wind_degrees:': resp["data"][0]["wind"]["degrees"],
                            'wind_speed:': resp["data"][0]["wind"]["speed_kph"],
                            'dewpoint:': resp["data"][0]["dewpoint"]["celsius"],
                            'humidity:': resp["data"][0]["humidity"]["percent"],
                            'pressure:': resp["data"][0]["barometer"]["hpa"],
                            'visibility:': resp["data"][0]["visibility"]["meters_float"],
                            'clouds1:': resp["data"][0]["clouds"][0]["text"],
                            'clouds1_level:': resp["data"][0]["clouds"][0]["meters"]}
                    except (KeyError, IndexError) as e:
                        weather = {
                            'airport:': resp["data"][0]["station"]["name"],
                            'category:': resp["data"][0]["flight_category"],
                            'datetime:': resp["data"][0]["observed"],
                            'temperature:': resp["data"][0]["temperature"]["celsius"],
                            'wind_degrees:': resp["data"][0]["wind"]["degrees"],
                            'wind_speed:': resp["data"][0]["wind"]["speed_kph"],
                            'dewpoint:': resp["data"][0]["dewpoint"]["celsius"],
                            'humidity:': resp["data"][0]["humidity"]["percent"],
                            'pressure:': resp["data"][0]["barometer"]["hpa"],
                            'visibility:': resp["data"][0]["visibility"]["meters_float"]
                    }



            def write_json(data, filename=str(airport)+'.json'):
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)

            with open(str(airport)+'.json') as f:
                data = json.load(f)
                temp = data["airport_info"]
                temp.append(weather)

            write_json(data)
        except requests.exceptions.HTTPError as e:
            print(e)



    for airport in airports:
        try:
            request(airport)
        except IndexError:
            pass



schedule.every(30).minutes.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)