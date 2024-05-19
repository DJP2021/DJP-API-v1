import json
import random
import string
import requests
import datetime
from openai import OpenAI
from fastapi.responses import JSONResponse
sms_man_token = "3ShawUalH6OguEx3ysrmXQ8fEcnMKhjM"
def validate_key(key):
    with open("data/valid_keys.json", "r") as f:
        keys = json.load(f)
    if key in keys:
        return 1
    else:
        return 0
    
def check_balance(key, costs):
    with open('data/valid_keys.json', 'r') as f:
        balance_keys = json.load(f)
        balance = balance_keys[key]
        if balance >= costs:
            newbalance = round(balance - costs, 1)
            balance_keys[key] = newbalance
            with open('data/valid_keys.json', 'w') as f:
                balance_keys = json.dump(balance_keys, f)
            return 1
        else:
            return 0

def register_user(userid):
    letters = string.ascii_letters + string.digits
    key = 'djp-'+''.join(random.choice(letters) for i in range(32))
    with open('data/valid_keys.json', 'r') as f:
        balance_keys = json.load(f)
    with open('data/valid_keys.json', 'w') as f:
        balance_keys[key] = 3
        balance_keys = json.dump(balance_keys, f)
    with open('data/registered_users.json', 'r') as f:
        userranks = json.load(f)
    with open('data/registered_users.json', 'w') as f:
        userranks[userid] = "Free"
        userranks = json.dump(userranks, f)
    with open('data/associated_keys.json', 'r') as f:
        userlist = json.load(f)
    with open('data/associated_keys.json', 'w') as f:
        userlist[userid] = key
        userlist = json.dump(userlist, f)
    with open('data/associated_users.json', 'r') as f:
        keylist = json.load(f)
    with open('data/associated_users.json', 'w') as f:
        keylist[key] = userid
        keylist = json.dump(keylist, f)
    with open('data/creation_dates.json', 'r') as f:
        dates = json.load(f)
    with open('data/creation_dates.json', 'w') as f:
        dates[userid] = str(datetime.datetime.now())
        dates = json.dump(dates, f)
    return key
        
        
def openai_request(prompt): 
    aiclient = OpenAI(base_url='https://api.pawan.krd/v1', api_key='pk-gHCzjrkRAWomHluzMScgECGuGRoSZOfDDoYjBmcauVoRZsTP') 
    response = aiclient.chat.completions.create(
  model="pai-001",
  messages=[{ 'role': 'user', 'content': prompt }],
  response_format= { "type":"json_object" }
)
    return response

def get_user_rank(userid):
    with open('data/registered_users.json', 'r') as f:
        userranks = json.load(f)
    if userid in userranks:
        rank = userranks[userid]
        return rank
    else:
        return 0

def set_user_rank(userid, rank):
    with open('data/registered_users.json', 'r') as f:
        userranks = json.load(f)
    if userid in userranks:
        userranks[userid] = rank
        with open('data/registered_users.json', 'w') as f:
            userranks = json.dump(userranks, f)
        return 1
    else:
        return 0

def get_creation_date(userid):
    with open('data/creation_dates.json', 'r') as f:
        dates = json.load(f)
    if userid in dates:
        date = dates[userid]
        return date
    else:
        return "Not saved"   
    
def get_user_key(userid):
    with open('data/associated_keys.json', 'r') as f:
        userkeys = json.load(f)
    if userid in userkeys:
        key = userkeys[userid]
        return key
    else:
        return 0
    
def get_user_number(userid):
    with open('data/associated_numbers.json', 'r') as f:
        numbers = json.load(f)
    if userid in numbers:
        number = numbers[userid]
        return number
    else:
        return 0
    
def get_user_notes(userid):
    with open('data/user_notes.json', 'r') as f:
        usernotes = json.load(f)
    if userid in usernotes:
        note = usernotes[userid]
        return note
    else:
        return "None"

def get_key_user(key):
    with open('data/associated_users.json', 'r') as f:
        keylist = json.load(f)
    if key in keylist:
        userid = keylist[key]
        return userid
    else:
        return 0    
    
def get_key_balance(key):
    with open('data/valid_keys.json', 'r') as f:
        balance_keys = json.load(f)
        if key in balance_keys:
            balance = balance_keys[key]
            return round(balance, 1)
        else:
            balance = "invalid"
            return balance
        
def validate_access(ID, level):
    with open('data/access_keys.json', 'r') as f:
        accesslist = json.load(f)
    if ID in accesslist:
        accesslevel = accesslist[ID]
        if accesslevel >= level:
            return 1
        else:
            return 0
    else:
        return -1
    
    
def rent_number(key):
    userid = get_key_user(key)
    check_balance(key, 2.5)
    country_id = 123
    application_id = 3
    url = f'https://api.sms-man.com/control/get-number?token={sms_man_token}&country_id={country_id}&application_id={application_id}'
    response = requests.get(url)
    data = response.json()
    phone_number = data['number']
    with open("data/associated_numbers.json", 'r') as f:
        numbers = json.load(f)
        numbers[userid] = phone_number
    with open("data/associated_numbers.json", "w") as f:
        numbers = json.dump(numbers, f)
    with open("data/number_request.json", "r") as f:
        numbersrequest = json.load(f)
        numbersrequest[phone_number] = data['request_id']
    with open("data/number_request.json", "w") as f:
        numbersrequest = json.dump(numbersrequest, f)
    return phone_number
    
def receival(key):
    userid = get_key_user(key)
    with open("data/associated_numbers.json", "r") as f:
        numbers = json.load(f)
    with open("data/number_request.json", "r") as f:
        nr = json.load(f)
    if userid in numbers:
        number = numbers[userid]
        if number in nr:
            requestnr = nr[number]
            url = f'https://api.sms-man.com/control/get-sms?token={sms_man_token}&request_id={requestnr}'
            response = requests.post(url)
            data = response.json()
            if 'sms_code' in data:
                smscode = data['sms_code']
                return smscode
            else:
                return 0
            
def check_permission(apikey, permlvl):
    userid = get_key_user(apikey)
    userrank = get_user_rank(userid)
    with open('src/assets/structure/ranklvl.json', 'r') as f:
        ranklevels = json.load(f)
    userlvl = ranklevels[userrank]
    if userlvl == 0:
        return -1
    if userlvl >= permlvl:
        return 1
    else:
        if userlvl == 1:
            return "verify"  
        else:
            return 0
