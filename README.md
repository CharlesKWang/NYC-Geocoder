# NYC-Geocoder
A geocoder module that uses the windows Geosupport Desktop edition, provided by the NYC Department of City Planning, to process geographic information within New York City using a python script.

 The Geosupport Desktop Edition package can be found at:
 https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-gde-home.page

 The full user programming guide can be found at: 
 https://www1.nyc.gov/assets/planning/download/pdf/data-maps/open-data/upg.pdf?r=17b
 
# Prerequisites
You'll need to download geosupport for windows.
The script is currently built to run with Python 2.7.

# Setup
In order to run the script, you may have to change the location of the NYCGeo.dll path to wherever you installed Geosupport. 

# Running
The script inputs and outputs csv files. It takes user inputs for the street address, borough, and zip code columns. Note that only one of the two, borough or zip code, are necessary.

More generally, the geo_coder function takes as inputs a house number, street name, borough, and zip code. It will output the two strings wa1 and wa2. The parser function can then be used to read these outputs.

An example would be:
```
#The address of Gotham Center, in LIC. 4 is the boro-code of Queens. The borough_transform function can interpret some common borough names/abbreviations for you.
(wa1, wa2) = geo_coder("42-09", 4, "28th st", 11101) 
output = Parser(wa1, wa2)
print output

{'2010 Census Block': '1050',
 '2010 Census Block Suffix': '',
 '2010 Census Tract': '19',
 'Assembly District': '37',
 'Atomic Polygon': '106',
 'B10SC First Borough and Street Code': '40764001010',
 'Bike Lane': '',
 'Borough Block Lot (BBL)': {'Borough code': '4',
  'Tax Block': '00420',
  'Tax Lot': '7501'},
 'Building Identification Number (BIN) of Input Address or NAP': '4538327',
 'City Council District': '26',
 'Community District': '402',
 'Community School District': '30',
 'Congressional District': '12',
 'DSNY Snow Priority Code': 'P',
 'Election District': '024',
 'First Borough Name': 'QUEENS',
 'House Number Display Format': '42-09',
 'House Number Sort Format': '100042009AA',
 'Hurricane Evacuation Zone (HEZ)': '5',
 'Latitude': '40.749641',
 'Longitude': '-73.939135',
 'Message': '',
 'NTA Name': 'Hunters Point-Sunnyside-West Maspeth',
 'Neighborhood Tabulation Area (NTA)': 'QN31',
 'Police Precinct': '108',
 'Roadway Type': '1',
 'Second Street Name Normalized': '28 STREET',
 'Spatial Coordinates of Segment': {'X Coordinate, High Address End': '1000963',
  'X Coordinate, Low Address End': '1001150',
  'Y Coordinate, High Address End': '0212157',
  'Y Coordinate, Low Address End': '0212462',
  'Z Coordinate, High Address End': '',
  'Z Coordinate, Low Address End': ''},
 'Spatial X': '1001114',
 'Spatial Y': '0212397',
 'State Senatorial District': '12',
 'USPS Preferred City Name': 'LONG ISLAND CITY',
 'X-Y Coordinates of Lot Centroid': '10011860212262',
 'Zip Code': '11101'}
```

Note that these are not all the fields given within the outputted wa1 and wa2. The list of fields, and their locations, can be found on pages 597-604
