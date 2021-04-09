# reconcile-gkg

This is a simple translation layer between Google's [Knowledge Graph Search API](https://developers.google.com/knowledge-graph) and (a subset of) the [Reconcilation Service API standard](https://reconciliation-api.github.io/specs/latest/). It's implemented as a proxy server using [Flask](https://flask.palletsprojects.com/en/1.1.x/).

## Usage

1. Clone this repository and install the requirements using `pip install -r requirements.txt`, preferably using a virtual environment.
2. Fill in the environment variable `GKG_API_KEY` in `.env` with a valid API key for the Knowledge Graph Search API.
3. Run the server with `flask run`.
4. Treat the local server (at `http://localhost:5000` by default) as if it was a reconciliation service endpoint, making requests using a client like OpenRefine or [reconciler](https://github.com/global-witness/reconciler). Requests will be translated and sent to the Google API.

## Limitations

At present the server only implements the following parameters from the Reconciliation Service API standard for requests: `query`, `type` and `limit`. All returned resuls are treated as succesful matches and the optional `features` array is not provided in responses.

## Deployment

The server can easily be deployed to the internet as an AWS Lambda function using the [Serverless](https://www.serverless.com/) framework. An example `serverless.yml` file is provided. 