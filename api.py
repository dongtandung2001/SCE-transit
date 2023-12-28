import requests
import json
from collections import defaultdict

API_URL = 'https://api.511.org/transit/StopMonitoring'
API_KEY = 'edf90b7a-72f7-4f06-900d-071f76d7de62'
stopIds = [63212, 63211]
results = []
for stopId in stopIds:
    url = f"{API_URL}?api_key={API_KEY}&agency=SC&format=json&stopCode={stopId}"
    print(url)
    res =  requests.get(url)
    decoded_res=res.text.encode().decode('utf-8-sig') 
    response = json.loads(decoded_res)

    lines = defaultdict(list)

    stops = response['ServiceDelivery']['StopMonitoringDelivery']


    for stop in stops['MonitoredStopVisit']:

        lines[stop['MonitoredVehicleJourney']['LineRef']].append(stop['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime'])

    response = {}

    response['id'] =  stops['MonitoredStopVisit'][0]['MonitoringRef']
    response['name'] = stops['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['StopPointName']
    response['predictions'] = []

    for line in lines:
        response['predictions'].append({
            "route": line,
            "times": lines[line]
        })


    results.append(response)
print(results)
