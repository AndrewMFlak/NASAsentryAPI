#====================== .env ========================>
import os
import requests
from os.path import join,dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

#====================================================>

#====================== MongoDB =====================>
import pymongo
try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
except pymongo.errors.ConnectionFailure as e:
    print(e)
db = myclient["NASAsentryAPI"]
col = db["NASAsentryAPIitems"]
#====================================================>

#password = os.getenv('test')
#print(password)
#print('password test completed')
import pandas as pd
import json
from pandas.io.json import json_normalize
# def jprint(obj):
    # create a formatted string of the Python JSON object
    #extractedContent = json.dumps(obj, sort_keys=True, indent=4)   
    # extractedContent = json.loads(obj)
    # for item in extractedContent:
        # print(item)
    #my_df = pd.DataFrame.from_dict(json_normalize(extractedContent),orient='columns')
    #my_df.rename(columns=lambda x: x.replace('.', ''), inplace=True)
extractedContent = requests.get("https://ssd-api.jpl.nasa.gov/sentry.api")
print(extractedContent)
# for item in extractedContent:
    # print(item)
parsed_json = (json.loads(extractedContent.text))
for item in parsed_json['data']:
    try: 
        db.NASAsentryAPIitems.update_one({'_id':item['id']},{'$set':item},upsert=True)
    except pymongo.errors.ConnectionFailure as e:
        print("Pymongo Insert Error: ",e)
    print(item)
    
# print(parsed_json)
# text = json.dumps(extractedContent, indent=4, sort_keys=True)
# print(text)
# jprint(response)

