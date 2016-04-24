import csv
from bs4 import BeautifulSoup
import requests

def get_url_soup_content(url):
  '''
  '''
  response = requests.get(url)
  if response.ok:
      return BeautifulSoup(response.text)

def get_data_from_table(tbl):
  variable_data = []
  for i in range(1,len(tbl.find_all('tr'))):
      starting_column = int(tbl.find_all('tr')[i].find('th').text)
      variable_name = tbl.find_all('tr')[i].find_all('td')[0].text
      field_length = int(tbl.find_all('tr')[i].find_all('td')[1].text)
      
      variable_data.append([starting_column,variable_name,field_length])
  
  return variable_data

def try_types(elem):
  if elem.isspace():
      return None
  try:
      return int(elem)
  except ValueError:
      return elem

def parse_data(variables_data):
  asc_file =  open('LLCP2014.ASC','r')
  #asc_file =  open('test.asc','r')
  read_data = asc_file.readlines()
  csv_list = []

  #for each line assign relevant values to keys in dictionary
  for line in read_data:
    curr_dict = {}

    for i in range(0,len(variables_data)):
      name = variables_data[i][1]
      start = (variables_data[i][0] - 1)
      end = ((variables_data[i][0] - 1) + variables_data[i][2])
      curr_dict[name] = try_types(line[start:end])
    csv_list.append(curr_dict)
  asc_file.close()

  with open('parsed_brfss.csv', 'w') as csvfile:
    fieldnames = []
    for i in range(0,len(variables_data)):
      fieldnames.append(variables_data[i][1])

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for line in csv_list:
        writer.writerow(line)
    csvfile.close()

if __name__ == '__main__':
  page = get_url_soup_content('http://www.cdc.gov/brfss/annual_data/2014/llcp_varlayout_14_onecolumn.html')
  var_data = get_data_from_table(page.find_all("div", {"class": "mSyndicate"})[1].find('table'))
  parse_data(var_data)