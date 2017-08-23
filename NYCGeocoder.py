#******************************************************************************
# Affiliation: NYCDoHMH
# Title: NYC Geocoder
# Author: Charles Wang
# 
# About: A geocoder module that uses the Geosupport Desktop edition, provided 
# by the NYC Department of City Planning, to process geographic information
# within New York City.
#
# The Geosupport Desktop Edition package can be found at:
# https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-gde-home.page
#
# The full user programming guide can be found at: 
# https://www1.nyc.gov/assets/planning/download/pdf/data-maps/open-data/upg.pdf?r=17b
#******************************************************************************

from ctypes import cdll
import csv
import sys
import os

NYCGeo = cdll.LoadLibrary(r'C:\Program Files\Geosupport Desktop Edition\Bin\NYCGeo.dll')

def rightpad(field, length):
    """Creates a string of specified length, either by adding whitespace to the right, or concatenating"""
    field = str(field)
    field_length = len(field)
    if field_length>length:
        field = field[:length]
    if field_length<length:
        while len(field)<length:
            field+=' '
    return field.upper()  

def geo_coder(house_number, boro_code, street_name, zip_code):   
    """given these four variables, inputs into the geocoder dll"""     
    wa1 = '1B{}{}{}{}{}C{}{}'.format(rightpad(house_number, 16), rightpad('', 38), boro_code, rightpad('', 10), rightpad(street_name, 32), rightpad('', 113), rightpad(zip_code, 5))
    wa1 = rightpad(wa1, 1200)
    wa2 = rightpad('', 4300)
    NYCGeo.NYCgeo(wa1, wa2)
    return wa1, wa2
    
    
def Parser(wa1, wa2):
    """Reads the output of the geocoder"""
    #Note that in the documentation, they start counting at position 1
    output = { 
          'First Borough Name': wa1[360 :369].strip(),
          'House Number Display Format': wa1[369: 385].strip(),
          'House Number Sort Format': wa1[385: 396].strip(),
          'B10SC First Borough and Street Code': wa1[396: 407].strip(),
          'Second Street Name Normalized': wa1[407:439].strip(),
          'Community District': wa2[149:152].strip(),
          'Zip Code': wa2[152:157].strip(),
          'Election District': wa2[157:160].strip(),
          'Assembly District': wa2[160:162].strip(),
          'Congressional District': wa2[163:165].strip(),
          'State Senatorial District': wa2[165:167].strip(),
          'City Council District': wa2[169:171].strip(),
          'Police Precinct': wa2[191:194].strip(),
          'Community School District': wa2[203:205].strip(),
          'Atomic Polygon': wa2[205: 208].strip(),
          '2010 Census Tract': wa2[223: 229].strip(),
          '2010 Census Block': wa2[229:233].strip(),
          '2010 Census Block Suffix': wa2[233].strip(),
          'Neighborhood Tabulation Area (NTA)': wa2[245:249].strip(),
          'DSNY Snow Priority Code': wa2[249].strip(),
          'Hurricane Evacuation Zone (HEZ)': wa2[260:262].strip(),
          'Spatial Coordinates of Segment': {'X Coordinate, Low Address End': wa2[313:320].strip(),
                                             'Y Coordinate, Low Address End': wa2[320:327].strip(),
                                             'Z Coordinate, Low Address End': wa2[327:334].strip(),
                                             'X Coordinate, High Address End': wa2[334:341].strip(),
                                             'Y Coordinate, High Address End': wa2[341:348].strip(),
                                             'Z Coordinate, High Address End': wa2[348:355].strip(),
                                              },
          'Roadway Type': wa2[444:446].strip(),
          'Bike Lane': wa2[486].strip(),
          'NTA Name': wa2[553: 628].strip(),
          'USPS Preferred City Name': wa2[628:653].strip(),
          'Latitude': wa2[653:662].strip(),
          'Longitude': wa2[662: 673].strip(),
          'Borough Block Lot (BBL)': {'Borough code': wa2[1533].strip(),
                                      'Tax Block': wa2[1534:1539].strip(),
                                      'Tax Lot': wa2[1539:1543].strip(),
                                      },
          'Building Identification Number (BIN) of Input Address or NAP': wa2[1581:1588].strip(),
          'X-Y Coordinates of Lot Centroid': wa2[1699:1713].strip(),
          'Spatial X': wa2[125:132].strip(),
          'Spatial Y': wa2[132:139].strip(),
          'Message': wa1[579:659].strip(),
        }
    return output

def borough_transform(Borough):
    """Translate borough names to borough codes. Names must be typed out in full"""
    boroughs = {'MANHATTAN': 1,
                 'BRONX': 2,
                 'BROOKLYN': 3,
                 'QUEENS': 4,
                 'STATEN ISLAND': 5,}
    if Borough.upper() in boroughs:
        return boroughs[Borough.upper()]
    else:
        return ' '

def geotransform(street_address_column, borough_column, zip_code_column, in_csv_file_loc, out_csv_file_loc):
    """reads a csv, and outputs a geocoded version"""
    with open(out_csv_file_loc, 'wb') as csv_new_file:
        fieldnames = ['2010 Census Block',
                     '2010 Census Block Suffix',
                     '2010 Census Tract',
                     'Assembly District',
                     'Atomic Polygon',
                     'B10SC First Borough and Street Code',
                     'Bike Lane',
                     'Borough Block Lot (BBL)',
                     'Building Identification Number (BIN) of Input Address or NAP',
                     'City Council District',
                     'Community District',
                     'Community School District',
                     'Congressional District',
                     'DSNY Snow Priority Code',
                     'Election District',
                     'First Borough Name',
                     'House Number Display Format',
                     'House Number Sort Format',
                     'Hurricane Evacuation Zone (HEZ)',
                     'Message',
                     'NTA Name',
                     'Neighborhood Tabulation Area (NTA)',
                     'Police Precinct',
                     'Roadway Type',
                     'Second Street Name Normalized',
                     'Spatial Coordinates of Segment',
                     'State Senatorial District',
                     'USPS Preferred City Name',
                     'X-Y Coordinates of Lot Centroid',
                     'Zip Code',
                     'Latitude',
                     'Longitude',
                     'Spatial X',
                     'Spatial Y']
        writer = csv.DictWriter(csv_new_file, fieldnames=fieldnames)
        writer.writeheader()
    
        with open(in_csv_file_loc, 'rb') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter = ',')
            for row in csvreader:
                full_address = row[street_address_column].strip()
                split_full_address = full_address.split(' ')
                house_number = split_full_address[0]
                borough = row[borough_column].strip()
                boro_code = borough_transform(borough)
                zip_code = row[zip_code_column].strip()
                street_name = ' '.join(split_full_address[1:])
    
                (wa1, wa2) = geo_coder(house_number, boro_code, street_name, zip_code)
                
                output = Parser(wa1, wa2)
                
                writer.writerow(output)
                

if __name__ == '__main__' :
    street_address_column = raw_input('Name of street address column: ')
    borough_column = raw_input('Name of borough column: ')
    zip_code_column = raw_input('Name of zipcode column: ')
    in_csv_file_loc = raw_input('csvfile location: ')
    out_csv_file_loc = raw_input('outfile name: ')
    if out_csv_file_loc[-4:] != '.csv':
        out_csv_file_loc += '.csv'
    
    local_path = sys.path[0]
    out_file = os.path.join(local_path, out_csv_file_loc)
    
    geotransform(street_address_column, borough_column, zip_code_column, in_csv_file_loc, out_csv_file_loc)
            
