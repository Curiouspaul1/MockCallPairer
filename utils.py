from dotenv import load_dotenv
import requests
import os
import csv
import random

load_dotenv()

owner, repo = os.getenv('OWNER'), os.getenv('REPO')
token = os.getenv('GITHUB_TOKEN')
BASE_URL = os.getenv('GH_URL')

def fetch_collaborators(page=1):
    _path = f'repos/{owner}/{repo}/collaborators?page={page}'
    resp = requests.get(
        url=BASE_URL+_path,
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
    )
    if resp.status_code == 200:
        # print(len(resp.json()))
        res = [
            obj['login']
            for obj in resp.json()
        ]
        # print('1', len(res))
        return res
    else:
        print(resp.status_code, resp.content)

def fetch_users(page=1):
    res = []
    ghUsers = fetch_collaborators(page)
    toPair = []
    # print('2', len(ghUsers))
    with open('data.csv', 'r') as data:
        mdata = csv.reader(data)
        for row in mdata:
            res.append({'gh': row[3].lower().strip(), 'wh': row[4]})
    
    for usr in ghUsers:
        for name in res:
            if usr.lower().strip() == name['gh'].lower():
                toPair.append(name['wh'])
    return toPair

# fetch_users(1)
# fetch_users(2)

def gen_pairs():
    final = []
    pairs = []
    for i in range(1,3):
        final.extend(fetch_users(i))
    check = []
    while final:
        try:
            pair = random.sample(final, k=2)
        except ValueError:
            print('Not enough values')
            break
        pairs.append(pair)
        check.append(pair)
        for p in pair:
            final.remove(p)
    return pairs

def update_file():
    with open('output.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['PersonA', 'PersonB'])
        _all = gen_pairs()
        for n in _all:
            writer.writerow(n)

def read_file():
    with open('output.csv', 'r') as data:
        mdata = csv.reader(data)
        res = []
        for n in mdata:
            if n and n[0].lower() != 'persona':
                res.append(n)
    return res


def get_topic():
    res = ''
    with open('topic.txt', 'r') as file:
        res += str(file.read())
    return res

print(get_topic())
