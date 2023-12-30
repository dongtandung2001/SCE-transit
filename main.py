from dataclasses import dataclass
import requests
import typing
import json
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import FastAPI

import pytz

app = FastAPI()

app.time = datetime.now()
app.cache = None
'''
/predictions

- return a list of of stops
- each stop has a stop id and name
- each stop has a list of predictions

- each prediction has a route name, 
- each prediction has an array of times for the 

'''
API_URL = 'https://api.511.org/transit/StopMonitoring'
API_KEY = 'edf90b7a-72f7-4f06-900d-071f76d7de62'

@dataclass
class Prediction:
    route: str
    times: typing.List[str]


@dataclass
class Stop:
    id: str
    name: str
    predictions: typing.List[Prediction]

@app.get('/predict')
async def predict():
    print(datetime.now() - app.time)
    if datetime.now() - app.time >= timedelta(minutes=10) or app.cache == None:
        print('call api...')
        results = []
        stopIds = [63211, 63212]
        for stopId in stopIds:
            url = f"{API_URL}?api_key={API_KEY}&agency=SC&format=json&stopCode={stopId}"
            res =  requests.get(url)
            decoded_res=res.text.encode().decode('utf-8-sig') 
            response = json.loads(decoded_res)

            lines = defaultdict(list)
            stops = response['ServiceDelivery']['StopMonitoringDelivery']

            for stop in stops['MonitoredStopVisit']:
                lines[stop['MonitoredVehicleJourney']['LineRef']] \
                .append(stop['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime'])

            id =  stops['MonitoredStopVisit'][0]['MonitoringRef']
            name = stops['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['StopPointName']
            s = Stop(id, name,[])
            
            for line in lines:
                s.predictions.append(Prediction(line,lines[line]))
            results.append(s)
        app.cache = results
        app.time = datetime.now()
        return results     
    else:
        print('cache used')
        return app.cache

