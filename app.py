#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://api.askvaidyo.com/api/v2/user "
    yql_url = baseurl
    yql_url.add_header('authorization', 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhc3NvY2lhdGlvbnMiOm51bGwsImN1c3RvbV9maWVsZCI6bnVsbCwicm9sZSI6W3sicm9sZV90eXBlX2lkIjoxMCwiY3JlYXRlZF90aW1lIjoiMjAxNy0wMS0zMVQxNDoyNToyNC42NjYwMTYiLCJpZCI6NDcsIm1vZGlmaWVkX3RpbWUiOiIyMDE3LTAxLTMxVDE0OjI1OjI0LjY2NjAxNiIsInJvbGVfYWN0aXZlIjoxLCJ1c2VyX2lkIjoxMTN9XSwiYWRkcmVzcyI6bnVsbCwidXNlcmRldGFpbHMiOnsiZXh0X3Byb3ZpZGVyX2lkIjpudWxsLCJpZCI6MTEzLCJ1dWlkIjoiVkFJRC1HVUVTVC0xIiwidXNlcm5hbWUiOiJndWVzdHVzZXJAdmFpZHlvLmNvbSJ9LCJwaG9uZSI6bnVsbCwicHJvZmlsZSI6bnVsbCwiZGV2aWNlIjpudWxsLCJpYXQiOjE0ODcxNjIzMTIsImVtYWlsIjpudWxsLCJjdXN0b21lciI6bnVsbCwic3RhdHVzIjoyMDB9.qCev5yw2kAdpd9VtMo_GdFVhmbPfknne2VuplUWmPcA=' )
    yql_url.add_header("Content-Type","application/json")
    yql_url.add_header("X-Select",'{"userid":402,"role":true,"email":true,"customer":true,"profile":true,"role":true,"device":true,"phone":true,"associations":true,"custom":true,"address":true}')
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res





def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "HI VAIDYO";

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {"Telegram":{data:speech}},
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
