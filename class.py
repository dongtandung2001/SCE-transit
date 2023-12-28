from dataclasses import dataclass

import typing


'''
/predictions

- return a list of of stops
- each stop has a stop id and name
- each stop has a list of predictions

- each prediction has a route name, 
- each prediction has an array of times for the 

'''

@dataclass
class Prediction:
    route: str
    times: typing.List[str]

@dataclass
class Stop:
    id: str
    name: str
    prediction: typing.List[Prediction]
