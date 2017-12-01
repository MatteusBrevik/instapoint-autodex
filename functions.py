from datetime import datetime  
from dateutil.relativedelta import relativedelta

def get_event(id):
    if int(id) not in range(0,10):
        return id

    return {
        0 : 'unknown',
        1 : 'vend paid with cash',
        2 : 'vend with credit',
        3 : 'vend with free credit',
        4 : 'mixed vend (amount free credit)',
        5 : 'mixed vend (amount credit)',
        6 : 'refunds after failed vend',
        7 : 'recharge',
        8 : 'free credit added',
        9 : 'free credit substituted'
    }[id]

def parse_datetime(hex):
    timestamp = int(hex, 16)
    date = datetime.fromtimestamp(timestamp) + relativedelta(years=28)
    return date.strftime('%Y-%m-%d %H:%M:%S')

def parse_event(input):
    date = parse_datetime(input[1])
    event = {
        'id' : int(input[2]),
        'name' : get_event(int(input[2]))
    }
    value = int(input[3])
    selection = int(input[4])
    user = int(input[5])
    credits = int(input[6])
    return {'date' : date, 'event' : event, 'value' : value, 'selection' : selection, 'user' : user, 'credits' : credits}

def split_by_n(text, n):
    return [text[i:i+n] for i in range(0, len(text), n)]

def parse_readout(input):
    return {
        'number' : int(input[1]),
        'datetime' : '20' + '-'.join(split_by_n(input[2], 2)) + ' ' + ':'.join(split_by_n(input[3], 2)),
        'previous' : '20' + '-'.join(split_by_n(input[5], 2)) + ' ' + ':'.join(split_by_n(input[6], 2))
    }