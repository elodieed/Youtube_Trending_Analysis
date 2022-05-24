import datetime
import json

def get_weekday(date):
    date = date.split('T')
    date = date[0].split('-')
    date = list(map(lambda x : int(x), date))
    x = datetime.datetime(date[0], date[1], date[2])
    return x.strftime("%w")

def get_only_date(date):
    date = date.split('T')
    return date[0]

def get_monthNyears(date):
    date = date.split('-')
    return str(date[0])+'-'+str(date[1])

def get_years(date):
    date = date.split('-')
    return str(date[0])

def listOfCategory():
    with open('./Data/FR_category_id.json') as json_data:
        data_dict = json.load(json_data)
    listCategory = list()
    for i in range(len(data_dict["items"])):
        id = data_dict["items"][i]["id"]
        name = data_dict["items"][i]['snippet']['title']
        listCategory += [[int(id), name]]
    return listCategory

def get_nameCategory(id):
    try :
        listCategory = listOfCategory()
        filter_object = list(filter(lambda x: id in x, listCategory))
        filter_object = filter_object[0][1]
    except:
        filter_object = None
    return filter_object


