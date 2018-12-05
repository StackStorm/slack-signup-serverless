import sys
import os
import json

# Import installed packages (in site-packages)
site_pkgs = os.path.join(os.path.dirname(os.path.realpath(__file__)), "site-packages")
sys.path.append(site_pkgs)

import requests
from urllib.parse import urlparse
from urllib.parse import urljoin

def endpoint(event, context):
    config = {}
    try:
        if isinstance(event, str):
            event = json.loads(event)

        print("Received event: " + json.dumps(event, indent=2))

        config['url'] = os.environ['URL']
        config['api_key'] = os.environ['API_KEY']
        tags = os.environ.get('TAGS')
    except KeyError:
        print ("ERROR: Environment variables URL and API_KEY must be set.")
        raise
    except ValueError as e:
        print ("ERROR: Can not parse `event`: '{}'\n{}").format(str(event), str(e))
        raise

    res = add_ac_contact(
        config,
        event.get('email'),
        country=event.get('country'),
        first_name=event.get('first_name'),
        last_name=event.get('last_name', ''),
        consentCheckBox=event.get('consent'),
        tags='')
    return {
        "statusCode": res[0],
        "message": res[1]
    }


def add_ac_contact(config, email, country, first_name='', last_name='', consentCheckBox='false', tags=''):
    url = urljoin(config['url'], 'admin/api.php')

    if consentCheckBox == 'true':
        consentCheckBox = "Please check the box if you are happy for StackStorm to keep you updated about our latest products, services and promotions via email."
    
    payload = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'field[%COUNTRY_GDPR%,0]': country,
        'field[%CONSENT_TO_PROCESSING%,0]': consentCheckBox,
        'tags': tags
    }
    query_params = {
        'api_key': config['api_key'],
        'api_action': 'contact_sync',
        'api_output': 'json'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    req = requests.Request('POST', url, params=query_params, headers=headers, data=payload)
    prepared = req.prepare()

    _pretty_print_POST(prepared)

    s = requests.Session()
    resp = s.send(prepared)

    print ("Status_code: {}\nContent: {}".format(resp.status_code, resp.content))

    result = resp.json()

    if resp.status_code == 200 and result['result_code'] != 0:
        print ("SUCCESS")
    else:
        failure_reason = (
            'Failed to create AC contact for {}: {} (status code: {})'.format(
                email, resp.text, resp.status_code))
        print (failure_reason)  
        raise Exception(failure_reason)

    return (resp.status_code, resp.text)


def _pretty_print_POST(req):
    print('{}\n{}\n{}\n\n{}\n{}'.format(
        '-----------REQUEST-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
        '-----------------------------',
    ))
