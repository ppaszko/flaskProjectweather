import requests
import json

from app import Airport


def all_request():
    """Requester for data."""
    airports = [T.name for T in Airport.query.all()]

    def request(airport):
        hdr = {"X-API-Key": "78beb76cf00149519431af799e"}
        req = requests.get('https://api.checkwx.com/metar/' + str(airport) + '/decoded', headers=hdr)
        req.raise_for_status()
        resp = json.loads(req.text)

        weather = {
            'airport:': resp["data"][0]["station"]["name"],
            'datetime:': resp["data"][0]["observed"]}

        try:
            weather['category:'] = resp["data"][0]["flight_category"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['temperature:'] = resp["data"][0]["temperature"]["celsius"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['wind_degrees:'] = resp["data"][0]["wind"]["degrees"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['wind_speed:'] = resp["data"][0]["wind"]["speed_kph"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['dewpoint:'] = resp["data"][0]["dewpoint"]["celsius"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['humidity:'] = resp["data"][0]["humidity"]["percent"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['pressure:'] = resp["data"][0]["barometer"]["hpa"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['visibility:'] = resp["data"][0]["visibility"]["meters_float"]

        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['ceiling:'] = resp["data"][0]["ceiling"]["text"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['ceiling_level:'] = resp["data"][0]["ceiling"]["meters"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['clouds1:'] = resp["data"][0]["clouds"][0]["text"]
        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['clouds1_level:'] = resp["data"][0]["clouds"][0]["meters"]

        except (KeyError, IndexError) as e:
            print(e)
            pass
        try:
            weather['conditions:'] = resp["data"][0]["conditions"][0]["text"]
        except (KeyError, IndexError) as e:
            print(e)
            pass

        def write_json(to_save, filename='/home/paszko/PycharmProjects/flaskProject/data/' + str(airport) + '.json'):
            with open(filename, 'w') as file:
                json.dump(to_save, file, indent=4)

        namefile='/home/paszko/PycharmProjects/flaskProject/data/' + str(airport) + '.json'
        with open(namefile, 'r') as f:
            data = json.load(f)
            f.close()
            temp = data
            temp.append(weather)
            write_json(temp)

    for airport in airports:
        try:
            request(airport)
        except (KeyError, IndexError) as e:
            print(e)
            pass


all_request()
