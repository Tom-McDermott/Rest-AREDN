
# Use REST API and JSON to query AREDN nodes about their status.
# Write output to file.  Python 3
#
# Version 1.0       December 17, 2021
# Copyright 2021, Thomas C. McDermott, N5EG
# Licensed under the GNU Public License (GPL), version 2, or at your choice any later version.
#


import requests
import json
from datetime import datetime


nodes = [
'N5EG-NSM2-EastMedford-Roof30-120',
'n7rbp-bm2-1',
'N7RBP-RKM2-1-Medford-OR',
'KE7MVI-NSM2-BLDY-S',
'K7BBS-NSM2-1',
'KI7ONK-NSM2-1',
'KI7RID-SM2XW-6-Medford',
'KG7HMZ-NSM2-3-RVAA',
'KC7HEX-NSM5XW-1-MEDFORD-OR-30-270',
'KC7HEX-NSM2-1-Medford-OR-30-003',
'KC7HEX-NSM2-2-Medford-OR-30-137',
'KC7HEX-NSM2-3-Medford-OR-10-180',
'KC7HEX-NSM2-4-Medford-OR-15-243',
'KC7HEX-CPE220-1-Medford-OR-30-315',
'KC7HEX-HAPAC-Medford-OR',
'KC7HEX-AM5G19-1-Medford-OR-15-222',
'KL7VK-RM2M-BALDY-20-0',
'KL7VK-LHG5XL-30-CP-25MAST-90',
'KL7VK-NSM2XW-LINK-TO-5GH',
'KL7VK-GL-AR300M-16-EXT-22-CP',
'KL7VK-HAPACL-200-CP',
'KL7VK-NSM5XW-24-BLKWELL-40TWR-SE',
'KL7VK-NSM5XW-25-BLKWELL-40TWR-W',
'KL7VK-PBLEM5XW-15-CPPD-40MAST-307',
'W9PCI-PB5-Roxy-15-280',
'W9PCI-LDF5-Roxy-mast15-270',
'W9PCI-HAPACL-RoxyAnn',
'W9PCI-RM2W-Roxy-15-230',
'W9PCI-NSM2-Roxy-15-180',
'W9PCI-M5-400ISO-15-180'
]

prefix = 'http://'
statrequest = '.local.mesh/cgi-bin/sysinfo.json?link_info=1'
now = datetime.now()


with open('/home/tom/outfile.dat', 'w', newline='') as outfile:

    outfile.write('Node status request.\nScan start : ' + str(now) + '\n')

    for node in nodes:
        try:
            r = requests.get(prefix+node+statrequest, timeout = 60)
            json = r.json()
            outfile.write('Node: ')
            outfile.write(node + '   Response Code: ' + str(r.status_code) + '\n')

            for key, value in json.items():
                if key == 'interfaces':     # it's a list of dictionaries
                    outfile.write('-----------------------\nInterfaces:')
                    for item in value:
                        #print(f'Item: {item}')
                        for key2 in item:
                            if key2 == 'mac':
                                outfile.write('\n  ')
                            outfile.write(' ' + key2 + ' : ' + item[key2] + '   ')
                    outfile.write('\n-----------------------\n')
                elif key == 'link_info':
                    outfile.write('\n-----------------------\nlink_info:')
                    for key2 in value:      # value is a dictionary with each key:value being IP:another dictionary
                        outfile.write('\n   ' + key2 + ' : ')
                        innervalue = value[key2]
                        #print('value = ', innervalue)
                        for key3 in innervalue:
                            outfile.write('   ' + key3 + '=' + str(innervalue[key3]))                        
                    outfile.write('\n-----------------------\n')
                else:
                    outfile.write(f'{key} : {value} \n')


            outfile.write('=========================================================================================\n')


        except Exception as e:
            outfile.write('Node: ')
            outfile.write(node + '    EXCEPTION\n')
            outfile.write(str(e) + '\n')
            outfile.write('=========================================================================================\n')


    outfile.write('\n')


