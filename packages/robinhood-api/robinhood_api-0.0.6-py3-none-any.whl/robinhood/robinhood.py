import json
import requests
import getpass
import os

session = requests.Session()
account_url = None


def oauth(payload):
    global session

    url = 'https://api.robinhood.com/oauth2/token/'
    r = session.post(url, json=payload)
    if r.status_code == 500:
        raise RuntimeError('Missing or incorrect credentials.')
    session.headers.pop('challenge_id', None)
    response = r.json()

    if 'access_token' in response:
        # save bearer_token and write to tokens.json
        session.headers['Authorization'] = 'Bearer ' + response['access_token']
        with open('tokens.json', 'w') as file:
            file.write(json.dumps({
                'bearer_token': response['access_token'],
                'refresh_token': response['refresh_token'],
                'device_token': payload['device_token']
            }))

    return r


def login(username: str = None, password: str = None, device_token: str = 'c77a7142-cc14-4bc0-a0ea-bdc9a2bf6e68',
          bearer_token: str = None, no_input: bool = False) -> str:
    """generates and returns OAuth2 bearer token"""
    global session

    if bearer_token is not None:
        session.headers['Authorization'] = 'Bearer ' + bearer_token
        if user():
            return bearer_token
        else:
            print('Invalid/expired bearer token')
            del session.headers['Authorization']
    # check if bearer token exists and is valid. create tokens.json if does not exist.
    if os.path.isfile('tokens.json'):
        with open('tokens.json', 'r') as file:
            try:
                tokens = json.loads(file.read())
                if 'bearer_token' in tokens:
                    bearer_token = tokens['bearer_token']
                    session.headers['Authorization'] = 'Bearer ' + bearer_token
                    if user():
                        return bearer_token
                    else:
                        del session.headers['Authorization']
            except json.decoder.JSONDecodeError:
                pass

    if username is None and not no_input:
        username = input('Enter email or username: ')
    if password is None and not no_input:
        password = getpass.getpass('Enter password: ')

    payload = {
        'grant_type': 'password',
        'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
        'device_token': device_token,
        'username': username,
        'password': password
    }

    r = oauth(payload)
    if r.status_code == 400:
        r = r.json()
        if 'detail' in r and r['detail'] == 'Request blocked, challenge type required.':
            challenge_type = None
            while challenge_type not in ['1', '2']:
                print('Unfamiliar device detected.')
                challenge_type = '1' if no_input else \
                    input("We're sending you a code to verify your login. Do you want us to:\n"
                          "  1: Text you the code\n"
                          "  2: Email it to you?\n")
                if challenge_type == '1':
                    print('Texting...')
                    payload['challenge_type'] = 'sms'
                elif challenge_type == '2':
                    print('Emailing...')
                    payload['challenge_type'] = 'email'
            r = oauth(payload)
            del payload['challenge_type']
            challenge_id = r.json()['challenge']['id']
            url = f'https://api.robinhood.com/challenge/{challenge_id}/respond/'
            verified = False
            while verified is False:
                verification_code = input('\nEnter your verification code: ')
                r = session.post(url, json={'response': verification_code}).json()
                if 'id' in r:
                    verified = True
                    print('\nVerified device.\n')
                else:
                    remaining_attempts = r['challenge']['remaining_attempts']
                    if remaining_attempts > 0:
                        print(f"Code is invalid. Remaining attempts: {remaining_attempts}.")
                    else:
                        raise RuntimeError('Verification failed.')
            session.headers['X-ROBINHOOD-CHALLENGE-RESPONSE-ID'] = challenge_id
            oauth(payload)
            del session.headers['X-ROBINHOOD-CHALLENGE-RESPONSE-ID']
        else:
            raise RuntimeError('Unable to log in with provided credentials.')

    elif r.status_code == 401:
        raise RuntimeError('Invalid bearer token.')

    return r.json()['access_token']


def user() -> bool:
    """checks whether user is logged in"""
    url = "https://api.robinhood.com/user/"
    r = session.get(url)
    if r.status_code == 401:
        # invalid bearer token
        return False
    else:
        print(f"Logged in as {r.json()['profile_name']}.\n")
        return True


def accounts():
    global account_url
    url = 'https://api.robinhood.com/accounts/'
    r = session.get(url).json()
    account_url = r['results'][0]['url']
    return r['results'][0]


def instruments(instrument=None, symbol=None):
    url = 'https://api.robinhood.com/instruments/'
    if instrument is not None:
        url += f'{instrument}/'
    if symbol is not None:
        url += f'?symbol={symbol}'
    r = session.get(url)
    return r.json()


def positions(nonzero: bool = True):
    url = 'https://api.robinhood.com/positions/'
    r = session.get(url, params={'nonzero': str(nonzero).lower()})
    if r.status_code == 401:
        raise RuntimeError(
            r.text + '\nYour bearer_token may have expired.')
    r = r.json()
    positions = {}
    for result in r['results']:
        instrument_url = result['instrument']
        r = session.get(instrument_url).json()
        positions[r['symbol']] = {
            'quantity': result['quantity'],
            'average_buy_price': result['average_buy_price']
        }
    return positions


def options_positions(nonzero: bool = True):
    url = 'https://api.robinhood.com/options/aggregate_positions/'
    r = session.get(url, params={'nonzero': nonzero})
    return r.json()


def live(account_number, span):
    if span not in {'day', 'week', 'month', 'year', 'all'}:
        raise RuntimeError(f"'{span}' is not valid as span.")
    url = 'https://api.robinhood.com/historical/portfolio_v2/live/'
    r = session.get(url, params={
        'account_number': account_number,
        'span': span,
        'from': 0
    })
    return r.json()


def fundamentals(instrument):
    url = f'https://api.robinhood.com/fundamentals/{instrument.upper()}/'
    r = session.get(url)
    return r.json()


def quotes(instrument):
    url = f'https://api.robinhood.com/marketdata/quotes/{instrument.upper()}/'
    r = session.get(url)
    return r.json()


def orders(price, symbol, instrument=None, quantity=1, type='market', side='buy', time_in_force='gfd',
           trigger='immediate', account=None):
    global account_url
    if account is None:
        account = account_url
    if instrument is None:
        instrument = fundamentals(symbol)['instrument']
    url = 'https://api.robinhood.com/orders/'
    r = session.post(url, json=locals())
    return r.json()
