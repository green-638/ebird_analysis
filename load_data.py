import os
import sys
import requests
import json
import pandas as pd 

# initialize csv with column names
def create_csv(path):
    with open(path, 'a') as f:
        f.write('checklist_id,species_code,species_name,loc_id,loc_name,date,quantity,country,subnational1,subnational2,first_name,last_name')


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
  

# initialize csv if empty or doesn't exist
path = input('CSV path: ')
# if file exists
if os.path.isfile(path):
    # if file is empty
    if os.path.getsize(path) == 0:
        create_csv(path)
        print(f'Added column labels to CSV')
else:
    create_csv(path)
    print('Initialized CSV')
    
df = pd.read_csv(path)


# api call
loc_num = 0
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
    # update CSV if changes were made
    if loc_num > 0:
      df.drop_duplicates(subset=['checklist_id', 'species_name', 'first_name', 'last_name'], inplace=True)
      df.to_csv(path, index=False)
      print(f'Partial data load complete. Following regions loaded: {locations[:loc_num]}')
      
    sys.exit()
    
  resp_json = json.loads(response.text)
  
  for report in resp_json:
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
                        'country': [report['countryName']],
                        'subnational1': [report['subnational1Name']],
                        'subnational2': [report['subnational2Name']],
                        'first_name': [report['firstName']],
                        'last_name': [report['lastName']]})
    
    df = pd.concat([df, row], ignore_index=True)    
  
  loc_num += 1

df.drop_duplicates(subset=['checklist_id', 'species_name', 'first_name', 'last_name'], inplace=True)

df.to_csv(path, index=False)

print('Data load complete')