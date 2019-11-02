from flask import Flask, request, jsonify
from wit import Wit 

app = Flask(__name__)
client = Wit('MM27TEXQYKGVRPNBNWLMYQOWSLQUDQJ6')

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

def format_entities(wit_response):
    resp = {}
    resp['command'] = get_with_default(wit_response['entities'], 'intent', None)

@app.route('/command-to-json')
def command_jsonify():    
    command = request.args.get('command', default = '', type = str)
    entities = client.message(command)
    resp = format_entities(entities)
    return jsonify(resp)

if __name__ == '__main__':
    app.run()
