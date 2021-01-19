import requests
import json

from app import Airport


def all_request():
    """Requester for data."""
    airports = [T.name for T in Airport.query.all()]

    def request(airport):
        hdr = {"X-API-Key": "78beb76cf00149519431af799e"}
        req = requests.get('https://api.checkwx.com/metar/' + str(airport) + '/decoded', headers=hdr)

        try:
            req.raise_for_status()
            resp = json.loads(req.text)
            print(resp)

            weather = {
                'airport:': resp["data"][0]["station"]["name"],
                'datetime:': resp["data"][0]["observed"]}
            if resp["data"][0]["flight_category"]:
                weather['category:'] = resp["data"][0]["flight_category"]
            if resp["data"][0]["temperature"]["celsius"]:
                weather['temperature:'] = resp["data"][0]["temperature"]["celsius"]
            if resp["data"][0]["wind"]["degrees"]:
                weather['wind_degrees:'] = resp["data"][0]["wind"]["degrees"]
            if resp["data"][0]["wind"]["speed_kph"]:
                weather['wind_speed:'] = resp["data"][0]["wind"]["speed_kph"]
            if resp["data"][0]["dewpoint"]["celsius"]:
                weather['dewpoint:'] = resp["data"][0]["dewpoint"]["celsius"]
            if resp["data"][0]["humidity"]["percent"]:
                weather['humidity:'] = resp["data"][0]["humidity"]["percent"]
            if resp["data"][0]["barometer"]["hpa"]:
                weather['pressure:'] = resp["data"][0]["barometer"]["hpa"]
            if resp["data"][0]["visibility"]["meters_float"]:
                weather['visibility:'] = resp["data"][0]["visibility"]["meters_float"]
            if resp["data"][0]["ceiling"]["text"]:
                weather['ceiling:'] = resp["data"][0]["ceiling"]["text"]
            if resp["data"][0]["ceiling"]["meters"]:
                weather['ceiling_level:'] = resp["data"][0]["ceiling"]["meters"]
            if resp["data"][0]["clouds"][0]["text"]:
                weather['clouds:'] = resp["data"][0]["clouds"][0]["text"]
            if resp["data"][0]["clouds"][0]["meters"]:
                weather['clouds1_level:'] = resp["data"][0]["clouds"][0]["meters"]
            if resp["data"][0]["conditions"][0]["text"]:
                weather['conditions:'] = resp["data"][0]["conditions"][0]["text"]

            def write_json(data, filename=str(airport) + '.json'):
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)

            with open(str(airport) + '.json') as f:
                data = json.load(f)
                temp = data["airport_info"]
                temp.append(weather)

            write_json(data)
        except requests.exceptions.HTTPError as e:
            print(e)

    for airport in airports:
        try:
            request(airport)
        except (KeyError, IndexError) as e:
            print(e)
            pass


all_request()
