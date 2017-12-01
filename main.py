import sys
import os
import re
import csv
from functions import *

if len(sys.argv) == 1:
    print('No file specified')
    exit(0) 

readout_start = False
readout_end = False

audits = {}

def run():
    data = None
    serial = None
    for line in open(sys.argv[1], 'r'):
        parts = line.strip().split('*')
        if line.startswith('DXS*'):
            data = {'readout' : {}, 'events' : [], 'location' : 0}
        elif line.startswith('EA3*'):
            data['readout'] = parse_readout(parts)
        elif line.startswith('DXE*'):
            if len(data['events']) > 0:
                if serial in audits:
                    audits[serial].append(data)
                else:
                    audits[serial] = [data]
            data = None
        elif line.startswith('ID1*'):
            serial = re.sub("[^0-9]", "", parts[1])

            if (int(serial) in [1447098, 1447109, 1447110, 1511002, 1447103]):
                serial = "20" + serial
            elif (int(serial) == 1411012):
                serial = "30" + serial

            data['location'] = re.sub("[^0-9]", "", parts[4])
        elif line.startswith('MR5*') and len(parts) == 7:
            data['events'].append(parse_event(parts))

    output  = open('output.csv', "w")
    writer = csv.writer(output, delimiter=',')
    writer.writerow(['serial', 'datetime', 'event', 'value', 'selection', 'user', 'credits', 'location', 'readout'])
    for key, value in audits.items():
        for i in range(0, len(value)):
            for event in value[i]['events']:
                #print(event['event']['name'])
                row = [key, event['date'], event['event']['name'], event['value'], event['selection'], event['user'], event['credits'], value[i]['location'], value[i]['readout']['number']]
                #print(row)
                writer.writerow(row)
    output.close()

run()

exit(0)

