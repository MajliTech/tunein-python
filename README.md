# tunein-python
An unofficial, highly experimental wrapper around TuneIn.
# pip?
Later. 
# How to use
Simple! Import `tunein` and you have 3 functions for interfacing with TuneIn:
1. `get_popular_stations()` - gets the popular stations in your area
query: str - the GuideId for the stations. Still working out what does this mean.
Returns a list with a dict for each radio station
keys: 
        - name: the name of the station
        - id  : the id you can use later in the library. scraped from GuideId of station
        - logo: an URL to station's image.
2. `get_station_metadata(id)` - Get stations data: logo, streaming urls, description, subtitle, frequency, language and if it's explicit
    id:str - a GuideId you obtained earlier

    returns a dict with all of the data mentioned above
    keys:
        - streams: a list of dicts looking like `{"reliability": int, "stream_url": str, "media_type": str, "bitrate": int}` (`{"reliability": 99, "stream_url": "http://www.rmfon.pl/tunein/tunein.p[...]", "media_type": "mp3", "bitrate": 128}`)
        - name: a str with the station name (RMF FM)
        - subtitle: in API called a slogan, a str with the station's subtitle (Najlepsza Muzyka / The Best Music)
        - frequency: if applicable, a float containing most likely FM frequency of the station. May be None (96.0)
        - description: a str with a long description of the station (Rozgłośnia nadaje program muzyczno-informacyjny, emitowany 24 godz...)
        - language: an str of the station's language (Polish)
        - lang: an str of a short-code of the language (pl)
3. `search_for_stations()` - Gets stations under the query provided
query: str - keywords for the stations

for returns, look at get_popular_stations
