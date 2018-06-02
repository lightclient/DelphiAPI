try:
    import ujson as json
except ImportError:
    import json


def loads(data):
    return json.loads(data)


def dumps(data):
    return json.dumps(data)



#helper function to objToDict()
def objListToDictList(l, exclude):
    return [ objToDict(ob, exclude) for ob in l ]


#helper function to objToSJON()
def objToDict(obj, exclude):
    #TODO: input validate
    attributes = {}
    for attr_name in dir(obj):
        attr = getattr(obj, attr_name)
        if not callable(attr) and not attr_name.startswith("_") and not attr_name in exclude:
            if isSimple(attr):
                attributes[attr_name] = attr
            elif isList(attr):
                attributes[attr_name] = objListToDictList(attr, exclude)
                #print('list: '+attr_name+': '+str(type(attr)) )
            elif isComplex(attr): #a complex object
                attributes[attr_name] = objToDict(attr, exclude)
                #print('complex: '+attr_name+': '+str(type(attr)) )
            else:
                'comment'
                #print('non-relevant: '+attr_name+': '+str(type(attr)) )
    return attributes

def listToJSON(lis, exclude):
    data = {'data': objListToDictList(lis, exclude), 'errors': []}
    return json.dumps(data)
            
def objToJSON(obj, exclude):
    data = {'data': objToDict(obj, exclude), 'errors': []}
    return json.dumps(data)


#TODO: de-hard-code?
def isSimple(obj):
    return (str(type(obj)) == '<class \'str\'>' or
            str(type(obj)) == '<class \'decimal.Decimal\'>' or
            str(type(obj)) == '<class \'datetime.datetime\'>' or
            str(type(obj)) == '<class \'int\'>' or
            str(type(obj)) == '<class \'bool\'>'
    )

def isList(obj):
    return (str(type(obj)) == '<class \'list\'>' or
            str(type(obj)) == '<class \'sqlalchemy.orm.collections.InstrumentedList\'>' 
    )

def isComplex(obj):
    return (str(type(obj))[8:30] == 'app.migrations.models.')
