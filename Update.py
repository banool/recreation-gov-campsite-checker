import json


f=open('facilities.json',)

output=json.load(f)
campgrounds = {}

for i in output['RECDATA']:
    campgrounds[i['FacilityName']] = i['FacilityID']


with open('parameters.py', 'w') as file:
    json.dump(campgrounds, file)