'''
Uses the python pacakage requests, see
http://docs.python-requests.org/en/latest/
'''

import json
import requests
import HTMLParser


def get_access_token(user, password, force_new=False):
    """Fetch old token from file or request new from server, return token"""
    print "Getting access token... ",
    try:
        assert force_new==False 
        with open(".%s_kahoot_token.txt" % user, 'r') as f: token = f.readline()
        print "Sucsessfully read old token from file"

    except:
        print "Failed to find token, generating new... ",

        # Kahoot login server
        url = 'http://db.kahoot.it/rest/authenticate'

        # Dictionary with login data
        authparams = {'username': user,
                      'password': password,
                      'grant_type': 'password'}

        r = requests.post(url, data=json.dumps(authparams), 
                          headers={'content-type':'application/json'})

        # Assert HTML status of response
        r.raise_for_status()
    
        # Fetch token from response object
        token = r.json()[u'access_token']

        # Write access token to a file for future use
        with open(".%s_token.txt" % user, 'w') as f:
            f.write(token)
        print "Done!"

    return token

def read_quiz_file(infile):
    """Read a .quiz file, return a list of dictionaries"""
    print "Parsing .quiz-file... ",
    with open(infile) as f:
        questions = eval(f.read())
    assert type(questions) == list
    assert type(questions[0]) == dict
    print "Success!"
    return questions
    
def make_quiz(questions, **kwargs):
    """Take a list of dictionaries, return kahoot quiz dictionary"""
    print "Turning questions into a Kahoot quiz object."

    # Parser for finding images in question text
    class ImgParser(HTMLParser.HTMLParser):
        def __init__(self):
            HTMLParser.HTMLParser.__init__(self)
            self.img_cnt = 0
            self.image_path = ""

        def handle_starttag(self, tag, attr):
            if tag.lower() == 'img':
                self.img_cnt += 1
                for att in attr:
                    if att[0].lower() == 'src':
                       self.img_path = att[1]

    # Parse questions
    for i, q in enumerate(questions):
        # Remove keys not relevant for Kahoot
        q.pop('no', None)
        q.pop('choice prefix', None)
        q.pop('question prefix', None)

        # Check for images in question text
        imgParser = ImgParser()
        imgParser.feed(q["question"])
        if imgParser.img_cnt == 1:
            q["image"] = self.upload_image(imgParser.img_path)
        elif imgParser.img_cnt > 1:
            print "Warning: Question %i contains more than one image, only"\
                  "one of them have been uploaded" % i
            q["image"] = self.upload_image(imgParser.img_path)
        else:
            q["image"] = ""

    # Parse choices
        for n, c in enumerate(q['choices']):
            q['choices'][n] = {"answer" : c[1],
                "correct" : c[0] == u'right'}

        # If there are more choices than 4, the rest are truncated
        if n+1 > 4:
            print "Warning: Kahoot only supports up to 4 answers, %i of the " \
                  "answers of question %i have been truncated!" % (n+1-4, i+1)
        
        # Additional question parameters
        q["numberOfAnswers"] = 4*(n+1 > 4) + (n+1)*(n+1 <= 4)
        q["questionFormat"] = 0
        q["time"] = 60000
        q["image"] = ""
        q["video"] = {"id" : "",
                      "startTime" : 0,
                      "endTime" : 0,
                      "service" : "youtube"}
        q["points"] = True

    # Add additional parameters
    # Default parameters
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
    # User-given
    for key in kwargs:
        if key==cover:
            self.upload_image()
        quiz[key] = kwargs[key]

    return quiz

def upload_quiz(quiz, token):
    """Upload a quiz (python dictionary) to Kahoot"""
    print "Uploading quiz to kahoot... ",

    # URL for making quizes
    url = "http://db.kahoot.it/rest/kahoots"
    
    r = requests.post(url, data=json.dumps(quiz), headers={
                            'content-type' : 'application/json',
                            'authorization' : token})

    # Assert HTML status of response
    r.raise_for_status()
    print "Success!"

def get_quiz(kahoot_id, token):
    """Fetch a given kahoot belonging to the user, returns dictionary"""
    print "Fetching given quiz from Kahoot"

    # URL for fetching specific kahoot
    url = "https://create.kahoot.it/rest/kahoots/%s" % kahoot_id
   
    r = requests.get(url, headers={
                     'content-type' : 'application/json',
                     'authorization' : token})

    # Assert HTML status of response
    r.raise_for_status()
    print "Success!"

    return r.json()

def get_all_quizes(token):
    """Fetch all kahoots belonging to user from server, return as list"""
    print "Fetching all quizes from Kahoot... ", 

    # URL for fetching all quizez
    url = "https://create.kahoot.it/rest/kahoots/browse/private?limit=30"

    r = requests.get(url, headers={
                     'content-type' : 'application/json',
                     'authorization' : token})
    
    # Assert HTML status of response
    r.raise_for_status()
    print "Success!"

    return r.json()[u'entities']

def delete_quiz(kahoot_id, token):
    """Delete kahoot of given id"""
    print "Deleting kahoot quiz..."

    # URL for deleting specific kahoot
    url = "https://create.kahoot.it/rest/kahoots/%s" % kahoot_id

    # HTML delete request
    r = requests.delete(url, headers={
                            'content-type' : 'application/json',
                            'authorization' : token})

    # Assert HTML status
    r.raise_for_status()
    print "Success!"

def delete_all_quizes(token):
    """Delete all kahoots on a given user"""
    print "This will delete ALL your kahoots permantently, are you sure? (Y/n)" 
    if raw_input("...") != "Y":
        print "Aborting"
        return

    quizes = get_all_quizes(token)
    for q in quizes:
        delete_quiz(q["uuid"], token)    

    print "Done deleting kahoots. User should now be clean."

def upload_image(img_filename, token):
    """Take image filename, post image to kahoot server, return url"""
    print "Uploading image to server... ",
    
    with open(img_filename, 'rb') as img:
        # URL for uploading media 
        url = "https://create.kahoot.it/media-api/media/upload"

        img_type = img_filename.split(".")[-1]
        if img_type not in ["gif", "jpg", "png", "jpeg"]:
            print "Error: %s is not a supported file-type for Kahoot."
            print "Make sure image file is png, jpg, jpeg or gif."
            print "Image has not been uploaded."
            return ""

        files = {'f': (img_filename, img, 'image/%s' % img_type)}

        r = requests.post(url, files=files, headers={'authorization' : token})   

    # Assert HTML status
    r.raise_for_status()

    print "success!"

    return r.json()["uri"]

user = 'jvbrink'
password = 'elektrolyse1'

token = get_access_token(user, password)

# Example of reading .quiz file, then making and uploading a kahoot quiz
questions = read_quiz_file("../demo-quiz/.test_jonas.quiz")
quiz = make_quiz(questions)
url = upload_image('../demo-quiz/fig/red_panda.jpg', token)
quiz["cover"] = url
for q in quiz["questions"]:
    q["image"] = url
upload_quiz(quiz, token)

pattern = r'''<img +src=["'](.+?)["']'''
import re
filenames = re.findall(pattern, html_text)
for filename in filenames:
   # upload filename
    
'''
# Example of fetching a pre-existing kahoot
q = get_all_quizes(token)
kahoot_id =  q[0]["uuid"]
quiz = get_quiz(kahoot_id, token)
'''

'''
delete_all_quizes(token)
'''