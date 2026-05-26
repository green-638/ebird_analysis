# ebird_analysis
This project creates a script that extracts data from the eBird API. The data is then analyzed with Excel.

## Requirements
- python 3.14.3
- pandas 3.0.3
- requests 2.34.2

## Using the script
Download load_data.py and install the libraries specified above in python 3.14.3. Upon running the script, you will be prompted to provide an eBird API key. An API request is then made to verify whether the key is valid. An invalid key will end the script. Next, you will be prompted to enter region codes to request data from. Region codes are IDs for a country (e.g. 'US'), subnational1 (e.g. a U.S. state: 'US-MD'), subnational2 (e.g. a county in a U.S. state: 'US-MD-005'), or location (a hotspot or private location e.g 'L295658'). If multiple region codes are entered, they must be separated by commas (e.g. CA,US-VA,US-MD-005). Next, you will be prompted to enter the number of days back to request data from, up to 30. Entering anything other than an integer 1-30 will end the script. Lastly, you will be prompted to enter the path of an existing CSV or the path where a CSV should be created. 
<br>
<br>
The script will make a request for each specified region code. If a region code is invalid, the CSV will be updated with all regions requested prior to invalid region. 
<br>
<br>
Note that API responses are limited to 10,000 results, so one request may not be enough to collect all data from a region. This effect is compounded by shared eBird checklists creating duplicate checklists for each eBird user. To mitigate this effect, consider collecting smaller sets of data and combining them afterwards. For example, data from Texas could be collected by requesting data from each county.