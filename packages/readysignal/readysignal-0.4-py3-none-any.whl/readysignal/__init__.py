import requests
import pandas as pd


def connect_to_readysignal(access_token, signal_id='', output=False):
    """
    creates connection to correct API URL to list signals, show signal
    details, and return complete signal data
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number, to show signal details
    or output full signal
    :param output: show signal data or not
    :return:
    """
    # list signals
    if not signal_id:
        url = 'http://app.readysignal.com/api/signals'
    # show signal details
    elif not output:
        url = f'http://app.readysignal.com/api/signals/{signal_id}'
    # show signal
    else:
        url = f'http://app.readysignal.com/api/signals/{signal_id}/output'

    headers = {'Authorization': 'Bearer ' + access_token,
               'Accept': 'application/json'}
    req = requests.get(url, headers=headers)

    return req


def list_signals(access_token):
    """
    lists all the signals associated with the user's access token
    :param access_token: user's unique access token
    :return: json of signals
    """
    conn = connect_to_readysignal(access_token)
    return conn.json()


def get_signal_details(access_token, signal_id):
    """
    shows the details for a specific signal
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: json of signal details
    """
    conn = connect_to_readysignal(access_token, signal_id)
    return conn.json()


def get_signal(access_token, signal_id):
    """
    returns a signal's data in json format
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: json of signal
    """
    conn = connect_to_readysignal(access_token, signal_id, output=True)
    return conn.json()


def get_signal_pandas(access_token, signal_id):
    """
    returns a signal's data as a Pandas DataFrame
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: Pandas DataFrame of signal
    """
    conn = connect_to_readysignal(access_token, signal_id, output=True)
    return pd.DataFrame.from_dict(conn.json()['data'])


def signal_to_csv(access_token, signal_id, file_name):
    """
    returns a signal's data as a Pandas DataFrame
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: Pandas DataFrame of signal
    """
    if '.' in file_name and '.csv' not in file_name:
        exit('Please enter a file name in the format: "signal" or "signal.csv"')
    elif '.' not in file_name:
        file_name += '.csv'

    conn = connect_to_readysignal(access_token, signal_id, output=True)
    df = pd.DataFrame.from_dict(conn.json()['data'])
    df.to_csv(file_name, index=False)
