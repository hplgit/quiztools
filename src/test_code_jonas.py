'''
Please reuse authorization token and sleep 5-10 sec
between each quiz uploaded
'''

import urllib
import httplib2
import json

def get_access_token(user, password):
    print "Getting access token... ",
    try:
        with open(".token.txt", 'r') as f: token = f.readline()
        print "Sucsessfully read old token from file"

    except:
        print "Failed to find token, generating new... ",

        # Kahoot login server
        url = 'http://db.kahoot.it/rest/authenticate'

        authparams = json.JSONEncoder().encode({
            'username': user,
            'password': password,
            'grant_type': 'password'
            })

        response, content = h.request(url, "POST", body=authparams, 
            headers={'content-type' : 'application/json'})

        decoded_content = json.loads(content.decode('utf8'))
        token = decoded_content['access_token']
        with open(".token.txt", 'w') as f:
            f.write(token)
        print "Done!"
    
    return token

def upload_quiz(quiz):
    print "Uploading quiz to kahoot... ",

    # URL for making quizes
    url = "http://db.kahoot.it/rest/kahoots"

    # We encode the dict object using json
    quiz = json.JSONEncoder().encode(quiz)
    
    # Push the quiz to kahoot
    response, content = h.request(url, "POST", body=quiz, headers={
                                  'content-type' : 'application/json',
                                  'authorization' : token})
    if response["status"] == "200":
        print "Success!"
    else:
        print "Something went wrong, quiz might not be uploaded correctly."

def get_all_quizes():
    '''
    Returns a list of kahoots
    '''
    print "Fetching all quizes from Kahoot user %s" 
    url = "https://create.kahoot.it/rest/kahoots/browse/private?limit=30"

    response, content = h.request(url, "GET", headers={
                              'content-type' : 'application/json',
                              'authorization' : token})

    if response["status"] != 200:
        print "Something went"

    return json.loads(content.decode('utf8'))[u'entities']
    
def read_quiz_file(infile):
    with open(infile) as f:
        questions = eval(f.read())
    assert type(questions) == list
    assert type(questions[0]) == dict

    for q in questions:
        q.pop('no', None)
        for i, c in enumerate(q['choices']):
            q['choices'][i] = {"answer" : c[1],
                "correct" : c[0] == u'right'}

        q["numberOfAnswers"] = i+1
        q["questionFormat"] = 1
        q["time"] = 60000
        q["image"] = ""
        q["video"] = {"id" : "",
                      "startTime" : 0,
                      "endTime" : 0,
                      "service" : "youtube"}
        q["points"] = True

        quiz = {
            'title' : 'Quiztools test quiz!',
             'questions' : questions,
             'quizType': 'quiz',
             'visibility': 0,  # 0: private, 1: public
             'type': 'quiz',
             'difficulty': 500,
             'audience': 'University',
             'language': 'English',
             'description': 'Test quiz of quiztools'
        }

    return quiz

user = 'jvbrink'
password = 'elektrolyse1'

h = httplib2.Http('.cache')
token = get_access_token(user, password)
quiz = read_quiz_file("../demo-quiz/.test_jonas.quiz")

print quiz
#upload_quiz(quiz)



# # The quiz is defined as a python dict object
# quiz_dict = {
#     'title': 'Quiztools test quiz!',
#     'questions': [
#         {
#             'question': 'What is the capital of Norway',
#             'questionFormat': 1,
#             'time': 60000, # milliseconds
#             'image' : "http://news.worldwild.org/wp-content/uploads/2008/09/red_panda.jpg",
#             # "video": {
#             #     "id": "",
#             #     "startTime": 0,
#             #     "endTime": 0,
#             #     "service": "youtube"
#             # },
#             'choices':[
#                 {
#                     'answer': 'Oslo',
#                     'correct': True
#                 },
#                 {
#                     'answer': 'Drammen',
#                     'correct': False
#                 }
#             ],
#             "points": True,
#             "numberOfAnswers": 2,
#         }
#     ],
#     'quizType': 'quiz',
#     'visibility': 0,  # 0: private, 1: public
#     'type': 'quiz',
#     'difficulty': 200,
#     'audience': 'University',
#     'language': 'English',
#     'description': 'Test quiz of quiztools'
# }




