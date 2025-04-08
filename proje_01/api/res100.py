import pymongo
import requests
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["NEWDATA"]
collection = db["NEWDATA"]

def res100(request, norttresponse, response_time):
    log = request.args.get('log')
    limit = request.args.get('limit')
    auth = request.args.get('auth')

    try:
        regex_query = {"url": {"$regex": log, "$options": "i"}}
        pipeline = [
            {"$match": regex_query},
            {"$sample": {"size": int(limit)}},
            {"$project": {"_id": 0}}
        ]
        results = collection.aggregate(pipeline)
        results_list = list(results)  
        return norttresponse(True, 'İşlem başarılı', results_list, 200, response_time)
    except Exception as e:
        return norttresponse(False, 'Error', None, 400, str(e))
