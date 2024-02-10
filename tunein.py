# Copyright (C) 2024 MajliTech
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/
import requests
class Errors:
    class TuneInError(BaseException):
        pass

def get_popular_stations(query: str = "v66") -> list:
    """
    Get popular stations in your area. 
    query: str - the GuideId for the stations. Still working out what does this mean.

    Returns a list with a dict for each radio station
    keys: 
        - name: the name of the station
        - id  : the id you can use later in the library. scraped from GuideId of station
        - logo: an URL to station's image.
    """
    stations_req = requests.get(f"https://api.tunein.com/profiles?isPrepopulateSearch=true&query={query}&formats=mp3,aac,ogg,flash,html,hls,wma&partnerId=RadioTime&version=6.1501")
    if not stations_req.ok:
        raise Errors.TuneInError(f"An HTTP error code has been returned: {stations_req.status_code}")
    stations_req=stations_req.json()["Items"][0]["Children"]
    response = []

    for i in stations_req:
        response.append({"name":i["Title"],"id":i["GuideId"],"logo":i["Image"]})
    return response
# https://api.tunein.com/profiles/<id>/contents?&formats=mp3,aac,ogg,flash,html,hls,wma&partnerId=RadioTime&version=6.1501
def get_station_metadata(id:str = None) -> dict or None:
    """
    Get stations data: logo, streaming urls, description, subtitle, frequency, language and if it's explicit
    id:str - a GuideId you obtained earlier

    returns a dict with all of the data mentioned above
    keys:
        - streams: a list of dicts looking like {"reliability": int, "stream_url": str, "media_type": str, "bitrate": int} ({"reliability": 99, "stream_url": "http://www.rmfon.pl/tunein/tunein.p[...]", "media_type": "mp3", "bitrate": 128})
        - name: a str with the station name (RMF FM)
        - subtitle: in API called a slogan, a str with the station's subtitle (Najlepsza Muzyka / The Best Music)
        - frequency: if applicable, a float containing most likely FM frequency of the station. May be None (96.0)
        - description: a str with a long description of the station (Rozgłośnia nadaje program muzyczno-informacyjny, emitowany 24 godz...)
        - language: an str of the station's language (Polish)
        - lang: an str of a short-code of the language (pl)

    """
    if id==None: return None
    # We have to hit 2 (or even more, like in s1217) URLs:
    # 1. https://opml.radiotime.com/Tune.ashx?id=s174766&formats=mp3,aac,ogg,flash,html,hls,wma&type=station&partnerId=RadioTime&version=6.1501&itemUrlScheme=secure&render=json  - for the streams
    # 2. https://api.tunein.com/profiles/s174766/contents?&formats=mp3,aac,ogg,flash,html,hls,wma&partnerId=RadioTime&version=6.1501 - all of the rest data
    response = {}
    # First - metadata
    metadata = requests.get(f"https://api.tunein.com/profiles/{id}/contents?&formats=mp3,aac,ogg,flash,html,hls,wma&partnerId=RadioTime&version=6.1501")
    if not metadata.ok:
        raise Errors.TuneInError(f"An HTTP error code has been returned: {metadata.status_code}")
    metadata = metadata.json()["Metadata"]["Properties"]
    response["name"]=metadata["GuideInfo"]["Name"]
    response["description"]=metadata["GuideInfo"]["Description"]
    response["subtitle"]=metadata["Station"]["Slogan"]
    response["language"]=metadata["Station"]["Language"]
    response["lang"]=metadata["Station"]["LanguageCode"]
    response["frequency"]= float(metadata["Station"]["Frequency"]) if metadata["Station"]["Frequency"] else None
    # then, streams
    response["streams"] = []
    for i in requests.get(f"https://opml.radiotime.com/Tune.ashx?id={id}&formats=mp3,aac,ogg,flash,html,hls,wma&type=station&partnerId=RadioTime&version=6.1501&itemUrlScheme=secure&render=json").json()["body"]:
        try:
            req = requests.head(i['url']).headers
            if not req["Content-Type"]=="application/json": raise
            req = requests.get(i['url']).json()
            for e in req["Streams"]:
                response["streams"].append({"stream_url":e["Url"],"reliability":int(e['Reliability']),"media_type":e["MediaType"].lower(),"bitrate":e["Bandwith"]})

        except:
            response["streams"].append({"stream_url":i["url"],"reliability":int(i['reliability']),"media_type":i["media_type"],"bitrate":i["bitrate"]})
    return response
def search_for_stations(query = None) -> list or None:
    """
    Gets stations under the query provided.
    """
    # https://api.tunein.com/profiles?fullTextSearch=true&query={query}&formats=mp3,aac,ogg,flash,html,hls,wma&partnerId=RadioTime&version=6.1501
    stations_req = requests.get(f"https://api.tunein.com/profiles?fullTextSearch=true&query={query}&formats=mp3,aac,ogg,flash,html,hls,wma&partnerId=RadioTime&version=6.1501")
    if not stations_req.ok:
        raise Errors.TuneInError(f"An HTTP error code has been returned: {stations_req.status_code}")
    stations_req=stations_req.json()["Items"]
    response = []
    for e in stations_req:
        for i in e["Children"]:
            if not i["Type"] == "Station": continue
            print(i,"\n----------\n\n")
            response.append({"name":i["AccessibilityTitle"],"id":i["GuideId"],"logo":i["Image"]})
    return response
