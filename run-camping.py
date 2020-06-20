from parameters import *
import os
import requests

output = ""
for i in parameters['charles']['parks']:
    output = output + i + " "

print (parameters['charles']['start-date'])
os.system('/usr/bin/python3 --version')
os.system('python camping.py --start-date '+ parameters['charles']['start-date']+ ' --end-date ' + parameters['charles']['end-date'] + ' --parks ' + output)