from flask import Flask, jsonify, request
import requests, json, os

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def reconcile():
    queries = request.form.get('queries')

    if not queries:
        return jsonify({'error': 'Please provide a batch of queries.'})
    
    else:
        queries = json.loads(queries)
        response = {}
        
        # Is there a neater way to do this?
        for k in queries.keys():
            response[k] = {}

        for k in queries.keys():
            payload = '{endpoint}?key={api_key}&query={query}'.format(
                endpoint = os.environ['GKG_ENDPOINT'],
                api_key = os.environ['GKG_API_KEY'],
                query = queries[k]['query'])

            if queries[k].get('type'):
                payload += '&types=' + ','.join([t for t in queries[k]['type'].split(',')])
            
            if queries[k].get('limit'):
                payload += '&limit=' + str(queries[k]['limit'])

            print(payload) 
            r = requests.get(payload)
            if r.status_code == 200:
                results = json.loads(r.text)['itemListElement']
            else:
                return jsonify({'error': r.status_code})

            response[k]['result'] = []
            for item in results:
                response[k]['result'].append(
                    {
                        "id": item['result'].get('@id'),
                        "name": item['result'].get('name'),
                        "description": item['result'].get('description'),
                        "type": [{"id": t, "name": t} for t in item['result'].get('@type')],
                        "score": item.get('resultScore'),
                        "match": True
                    })
                
        return jsonify(response)