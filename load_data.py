import os
import sys
import requests
import json
import pandas as pd 

# initialize csv with column names
def create_csv(path):
    with open(path, 'a') as f:
        f.write('checklist_id,species_code,species_name,loc_id,loc_name,date,quantity,subnational1,subnational2,first_name,last_name')


# input api key
token = input('eBird API key: ')
# test request
url = 'https://api.ebird.org/v2/ref/region/info/US-MD'
payload={}
headers = {
  'X-eBirdApiToken': token
}
# get request status code
status_code = requests.request("GET", url, headers=headers, data=payload).status_code
# exit program if invalid
if status_code != 200:
  print('Invalid key')
  sys.exit()

# input locations to pull data from
locations = input('Region codes, separated by commas (e.g. US,US-MD,US-MD-005,L295658): ').split(',')

# input how many days back to pull data from
days = int(input('# of days back to pull data from (<=30): '))
if days > 30:
  print('Reports cannot be over 30 days old')
  sys.exit()


all_responses = []
# api call
for loc in locations:
  url = f'https://api.ebird.org/v2/data/obs/{loc}/recent/notable?back={days}&detail=full'
  headers = {
    'X-eBirdApiToken': token
  }
  
  response = requests.request("GET", url, headers=headers, data=payload)
  # get request status code
  status_code = response.status_code
  # exit program if invalid
  if status_code != 200:
    print(f'"{loc}" is an invalid region code')
    sys.exit()
    
  resp_json = json.loads(response.text)
  all_responses += resp_json
  
  
# initialize csv if empty or doesn't exist
path = input('CSV path: ')
# if file exists
if os.path.isfile(path):
    # if file is empty
    if os.path.getsize(path) == 0:
        create_csv(path)
else:
    create_csv(path)
  

df = pd.read_csv(path)
# iterate through each location's reports
for report in all_responses:
  keys = report.keys()
  # add 'X' to reports with no species quantity
  if 'howMany' not in keys:
    report['howMany'] = 'X'
  # mark subnational1 and subnational2 as N/A when necessary
  if 'subnational1Name' not in keys:
    report['subnational1Name'] = 'N/A'
  if 'subnational2Name' not in keys:
    report['subnational2Name'] = 'N/A'
    
  # create new row
  row = pd.DataFrame({'checklist_id': [report['subId']],
                      'species_code': [report['speciesCode']],
                      'species_name': [report['comName']],
                      'loc_id': [report['locId']],
                      'loc_name': [report['locName']],
                      'date': [report['obsDt']],
                      'quantity': [report['howMany']],
                      'subnational1': [report['subnational1Name']],
                      'subnational2': [report['subnational2Name']],
                      'first_name': [report['firstName']],
                      'last_name': [report['lastName']]})
  
  df = pd.concat([df, row], ignore_index=True)    
    
df = df.drop_duplicates(keep='last', ignore_index=True)
df.to_csv(path)

print('Data load complete')