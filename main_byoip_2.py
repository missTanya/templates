
import json
from jinja2 import Template, Environment, FileSystemLoader
import jinja2
import os
import sys
import csv
from datetime import datetime
from pprint import pprint


class byoip:

    def __init__(self, file, temp):
    	"""This is just a constructor
    	"""
    	if '.csv' in file:
    		self.file = file
    	else:
    		self.file = file + '.csv'  #add .csv extension
    	self.temp = temp   #not used, reserved for future extension

    def csvParser(self, file):
    	"""This will convert a csv file to a dictionary data
    	- file: csv file
    	- returns a dictionary of data
    	"""
    	outer_dict = {} #--> used
    	with open(file, 'r') as csv_file:
    		reader = csv.DictReader(csv_file, delimiter=',')
    		for row in reader:
    			if row['customer_name'] in outer_dict.keys():
    				cust = row['customer_name']
    				temp_dict_new = {}  #always set to null
    				temp_dict_new = row.copy()
    				outer_dict[cust].append(temp_dict_new)
    			else:
    				cust = row['customer_name']
    				row.pop('customer_name', None)
    				temp_dict = {}  #always set to null
    				temp_dict = row.copy()
    				temp_list = [] #always set to null
    				temp_list.append(temp_dict)
    				outer_dict[cust] = temp_list
    	return outer_dict

class main:
	"""This will generate the template for BYOIP pillar
	"""
	file = 'sample002.csv'  #not improved yet, will need to manually set this on the code
	obj2 = byoip(file, 'sample')
	pillar_dict = byoip.csvParser(obj2, file)

	t = jinja2.Template(

"""
	{# THIS WILL GENERATE BYOIP PILLAR #}
byoip:
  announcement:
	{%- for customer, list_of_dict in dict_new.items() %}
    - {{ customer }}:
      {%- for item in list_of_dict %}
      - prefix: {{ item['prefix'] }}
        as: {{ item['asn'] }}
        services:
          - {{ item['service'] }}
        state: active
  	    {%- if item['ipv4_bool'] == '1' %}
        ondemand: true
  	    {%- else %}
        family: 6
  	    {%- endif %}
  	  {%- endfor %}
	{%- endfor %}

firewall:
	{%- for customer, list_of_dict in dict_new.items() %}
  - {{ customer }}:
  	  {%- for item in list_of_dict %}
    - prefix: {{ item['prefix'] }}
      service: {{ item['service'] }}
  	    {%- if item['ipv4_bool'] == '0' %}
      family: 6
  	    {%- endif %}
  	  {%- endfor %}
	{%- endfor %}
""")
	#This will pass the dictionary to the template
	print(t.render(dict_new=pillar_dict))


if __name__ == '__main__':
    main()