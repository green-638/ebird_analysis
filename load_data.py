from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd 

# initialize csv with column names
def create_csv():
    with open('/Volumes/Crucial 1TB SSD/datasets/ebird/ebirddata.csv', 'a') as f:
        f.write('checklist_id,species_code,species_name,loc_id,loc_name,date,quantity,subnational1,subnational2,first_name,last_name')


# load env file
load_dotenv()

# get token from .env
token = os.getenv('ebirdtoken')
# assign locations to pull data from
locations = ['US-MD', 'US-DC', 'US-DE', 'US-VA']
# hold api responses
all_responses = []

# api call
for loc in locations:
  url = f'https://api.ebird.org/v2/data/obs/{loc}/recent/notable?back=30&detail=full'
  payload={}
  headers = {
    'X-eBirdApiToken': token
  }

  response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
  all_responses += response
  
  
# initialize csv
# if file exists
if os.path.isfile('/Volumes/Crucial 1TB SSD/datasets/ebird/ebirddata.csv'):
    # if file is empty
    if os.path.getsize('/Volumes/Crucial 1TB SSD/datasets/ebird/ebirddata.csv') == 0:
        create_csv()
else:
    create_csv()
  

df = pd.read_csv('/Volumes/Crucial 1TB SSD/datasets/ebird/ebirddata.csv')

# iterate through each location's reports
for report in all_responses:
  keys = report.keys()
  # add X to reports with no species quantity
  if 'howMany' not in keys:
    report['howMany'] = 'X'
    
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
df.to_csv('/Volumes/Crucial 1TB SSD/datasets/ebird/ebirddata.csv')

print('Data load complete')