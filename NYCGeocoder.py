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
    output = { 
          'firstBoroName': wa1[360 :369].strip(),
          'houseNumberDisplay': wa1[369: 385].strip(),
          'houseNumberSort': wa1[385: 396].strip(),
          'firstBoroStreetCode': wa1[395: 11].strip(),
          'firstStreetNameNormalized': wa1[407:439].strip(),
          'communityDistrict': wa2[149: 152].strip(),
          'zipCode': wa2[152:157].strip(),
          'electionDistrict': wa2[157:160].strip(),
          'atomicPolygon': wa2[205: 208].strip(),
          'censusTract10': wa2[223: 229].strip(),
          'censusBlock10': wa2[229:233].strip(),
          'ntaName': wa2[553: 628].strip(),
          'latitude': wa2[653:662].strip(),
          'longitude': wa2[662: 673].strip(),
          'bbl': wa2[1533:1543].strip(),
          'spatialX': wa2[125:132].strip(),
          'spatialY': wa2[132:139].strip(),
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
        fieldnames = ['firstBoroName', 'houseNumberDisplay', 'houseNumberSort', 'firstBoroStreetCode',
              'firstStreetNameNormalized', 'communityDistrict', 'zipCode', 'electionDistrict',
              'atomicPolygon', 'censusTract10', 'censusBlock10', 'ntaName', 'latitude', 'longitude', 'bbl', 'spatialX', 'spatialY',
               'Message',]
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
            