import json
import urllib
import httplib2

url = 'http://db.kahoot.it/rest/authenticate'

authparams = json.JSONEncoder().encode({
        'username': 'XXXuser',
        'password': 'XXXpass',
        'grant_type': 'password'
    })
         
h = httplib2.Http('.cache')

print authparams

(headers, resp) = h.request(url, "POST", body=authparams, headers={'content-type': 'application/json'})

print resp

data = json.loads(resp.decode('utf8'))

token = data['access_token']

print(token)

url = 'http://db.kahoot.it/rest/kahoots'

quiz = json.JSONEncoder().encode({
        'title': 'testtitle',
        'questions': [ {
            'question': 'q1',
            'questionFormat': 0,
            'time': 30000,
            'choices': [ {
                    'answer': 'a',
                    'correct': 'false'
                }, {
                    'answer': 'b',
                    'correct': 'true'
                }]
        } ],
        'quizType': 'quiz',
        'visibility': 0,
        'type': 'quiz',
        'difficulty': 500,
        'audience': 'University',
        'language': 'English',
        'description': 'Description'
    })

(headers, resp) = h.request(url, "POST", body=quiz, headers={'content-type': 'application/json', 'Authorization': token})

print resp
