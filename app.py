from flask import Flask, request, jsonify
from wit import Wit 
from fuzzywuzzy import process
import nltk
from nltk.corpus import wordnet

app = Flask(__name__)
client = Wit('MM27TEXQYKGVRPNBNWLMYQOWSLQUDQJ6')

nltk.download('wordnet')

class type:
    as_is = "as-is"
    query = "query"
    
def get_with_default(collection, key, default):
    if key in collection:
        return collection[key]
    return default

def get_nth_value(collection, n):
    if len(collection) < n:
        return None
    nth = collection[n]
    if 'value' in nth:
        return nth['value']
    return None

def as_is(string):
    resp = {}
    formatted_resp = {}
    resp['type'] = type.as_is
    formatted_resp["body"] = string 
    resp["result"] = formatted_resp
    return resp

def nlu_stuff(table_wit, table_list):
    SynArr=[]
    HypoArr=[]
    countsOfWords = {}
    
    SArr = wordnet.synsets(table_wit)
    
    for syn in SArr:
        for hypo in syn.hyponyms():
            HypoArr.append(hypo)
       
    for syn in HypoArr:
        for lem in syn.lemmas():
            SynArr.append(lem.name())
       
    for syn in SynArr:
        highest = process.extractOne(syn,table_list)
        word = highest[0]
        if word in countsOfWords:
            countsOfWords[word] = countsOfWords[word] + 1
        else:
            countsOfWords[word] = 0
    highest = 0
    for word in countsOfWords:
        count = countsOfWords[word]
        if count > highest:
            highest = count
            table_actual =  word
    return table_actual

def format_entities(wit_response, req_body):
    wit_resp = {}
    formatted_resp = {}
    resp = {}
    table_list = []
    for db in req_body:
        print(db)
        for tables in db["tables"]:
            print(db["tables"])
            table_list.append(tables)
    print(get_nth_value(get_with_default(wit_response["entities"], "table_name", None), 0))
    print(table_list)
    wit_resp = {"command" : get_with_default(wit_response["entities"], "intent", None), 
                "table_name" : nlu_stuff(get_nth_value(get_with_default(wit_response["entities"], "table_name", None), 0), table_list),
                "conditions" : get_with_default(wit_response["entities"], "datetime", None)}
    formatted_resp = {"command_type" : get_nth_value(wit_resp["command"], 0), 
                      "table_name" : wit_resp["table_name"],
                      "conditions" : get_nth_value(wit_resp["conditions"], 0)}
    for db in req_body:
        if formatted_resp["table_name"] in db["tables"]:
            formatted_resp["db_name"] = db["database"]
    resp = {"type" : type.query, "result" : formatted_resp}
    return resp

@app.route('/command-to-json', methods=['POST'])
def command_jsonify():
    body = request.get_json() 
    print(body)
    print("-------------")
    if body is None:
        return as_is("Oops! No DB found.")
    command = request.args.get('command', default = '', type = str)
    entities = client.message(command)
    resp = format_entities(entities, body)
    return jsonify(resp)

if __name__ == '__main__':
    app.run()
