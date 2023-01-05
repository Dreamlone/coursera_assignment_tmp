import os
from typing import List, Dict
from collections import Counter

import datetime

import requests

# Keep secrets not in constants but in env variables in IDE
SERVICE_KEY = os.environ.get('SERVICE_KEY')


def response_to_ages_converting(friends: List[Dict]):
    """ Convert output with friends information """
    # Filter people with available 'bdate' field
    friends = list(filter(lambda x: 'bdate' in x.keys(), friends))
    print(f'Number of friends to with filled "bdate" field: {len(friends)}')
    current_date = datetime.datetime.now()

    ages = []
    for item in friends:
        bdate = item['bdate']
        if len(bdate.split('.')) == 3:
            datetime_bdate = datetime.datetime.strptime(bdate, "%d.%m.%Y")
            years_age = current_date.year - datetime_bdate.year
            ages.append(years_age)

    # Sort before descending ensure that the list will be sorted in ascending
    # order by the first key
    ages.sort()

    print(f'Ages: {ages}\n')
    friends_number_by_age = dict(Counter(ages))
    ages = list((age, friends_number) for age, friends_number in friends_number_by_age.items())

    ages = sorted(ages, key=lambda x: x[1], reverse=True)
    return ages


def calc_age(uid: str):
    """
    Calculate ages distribution for desired user

    :param uid: user ID
    """

    # Get information about user
    url = 'https://api.vk.com/method/users.get'
    params = {'v': '5.81', 'access_token': SERVICE_KEY, 'user_ids': uid}
    user_info = requests.request("GET", url, params=params)
    current_uid_info = eval(user_info.text)['response'][0]
    # Get identifier in integer form
    integer_id = int(current_uid_info['id'])
    print(f'Information about user {uid}: {current_uid_info}')

    # Get information about user's friends
    url = 'https://api.vk.com/method/friends.get'
    params = {'v': '5.81', 'access_token': SERVICE_KEY,
              'user_id': integer_id, 'fields': 'bdate'}
    friends_info = requests.request("GET", url, params=params)
    friends_info = eval(friends_info.text)['response']

    print(f'Full number of friends to process: {friends_info["count"]}')
    return response_to_ages_converting(friends_info['items'])


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
