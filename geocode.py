import requests, re

def getGeo(address):
    address = re.sub(r'\W+', '%20', address)
    url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/%s.json?access_token=pk.eyJ1Ijoib3Blbi1hZGRyZXNzZXMiLCJhIjoiSGx0a1B1NCJ9.2O1QelK6jnFXfDznC2pNSw&limit=5' % address
    sendback = requests.get(url).json()
    results = sendback['features']
    bestresult = [r for r in results if 'address' in r['place_type'] and r['relevance']>0.6][0]
    return {'address':bestresult['place_name'], 'latitude':bestresult['geometry']['coordinates'][1], 'longitude':bestresult['geometry']['coordinates'][0]}
