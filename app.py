from flask import Flask, jsonify, request
import requests, json, os
import random

app = Flask(__name__)

def make_request(payload, api_key):
    payload += '&key=' + api_key
    r = requests.get(payload)
    random_number = random.randint(1, 11)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return {'error': r.status_code}

@app.route('/', methods = ['POST'])
def reconcile():
    queries = request.form.get('queries')

    if not queries:
        return jsonify({'error': 'Please provide a batch of queries.'})
    
    queries = json.loads(queries)
    response = dict.fromkeys(queries.keys(), {})
        
    for query_id, query in queries.items():
        payload = '{endpoint}?query={query}'.format(
            endpoint = os.environ.get('GKG_ENDPOINT'),
            query = query['query'])

        if query.get('type'):
            payload += '&types=' + ','.join([t for t in query['type'].split(',')])
            
        if query.get('limit'):
            payload += '&limit=' + str(query['limit'])

        results = make_request(payload, os.environ.get('GKG_API_KEY'))

        if results.get('error'):
            return jsonify(results)
        
        response[query_id]['result'] = []
            
        for item in results['itemListElement']:
            # Exclude result items without a type
            if item['result'].get('@type'):
                response[query_id]['result'].append({
                    'id': item['result'].get('@id'),
                    'name': item['result'].get('name'),
                    'description': item['result'].get('description'),
                    'type': [{'id': t, 'name': t} for t in item['result'].get('@type')],
                    'score': item.get('resultScore'),
                    'match': True
                })
                
        return jsonify(response)