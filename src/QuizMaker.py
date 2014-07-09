"""
Uses the python pacakge requests, see
http://docs.python-requests.org/en/latest/
"""

import json
import requests
import getpass

class QuizMaker:
    """Base class for quiz makers."""
    def __login(self, user, password):
        """Get access to given site."""
        raise NotImplementedError

    def get_quiz(self, quiz_id):
        """Return quiz with given id."""
        raise NotImplementedError

    def get_all_quizzes(self):
        """Return list of all quizzes belonging to user."""
        raise NotImplementedError

    def upload_quiz(self, quiz):
        """Take quiz-object as input, upload to site."""
        raise NotImplementedError

    def delete_quiz(self, quiz_id):
        """Delete quiz with given id."""
        raise NotImplementedError

    def delete_all_quizzes(self):
        """Deletes all quizzes belonging to user."""
        raise NotImplementedError

    def pop_quiz(self, quiz_id):
        """Deletes quiz of given id and returns it to user."""
        quiz = self.get_quiz(quiz_id)
        self.delete_quiz(quiz_id)
        return quiz

    def read_quiz_file(self, quiz_file):
        """Read a .quiz file, return a list of dictionaries."""
        print "Reading .quiz-file... ",
        with open(quiz_file) as f:
            questions = eval(f.read())
        assert type(questions) == list
        assert type(questions[0]) == dict
        print "success!"
        return questions

    def make_quiz(self, questions, **kwargs):
        """Take a list of dictionaries as found when parsing .quiz-file,
        return a quiz-object specialized for the given website."""
        raise NotImplementedError

"""
___Kahoot syntax guide___

The "quiz" object is used as input to upload_quiz, and as output from
get_quiz and get_quizzes with KahootQuizMaker. It is a python dictionary
with various key:value parameters. One of these keys are "questions", which
should be a list of dictionaries corresponding to each question. 

___PARAMETERS___
title - string, title of the quiz
type - string, not in use, set it to 'quiz'
quizType - string, "quiz"/"poll"/"survey"
visiblity - int, 0 is private, 1 is public
language - string, language of the quiz
description - string, metadata
audience - string, metadata
cover - string, url to cover image
        Note: images must be uploaded to kahoot servers
        when using the cover kwarg to make_quiz, give the local
        image file as string, and the method will upload it to
        the kahoot server and attach the url automatically

Question params
  question - string, question text
  questionFormat - int, 0 for image, 1 for video
  time - time for question in ms
  points - boolean, defines if the question is worth any points
  numberOfAnswers - int, from 2 to 4
  image - string, url to image (must be uploaded to kahoot servers)

  choices - list of dictionary
    answer - string, text of answer
    correct - boolean

  # Warning, video is an experimental feature
  video - dictionary, video to be shown in the background
    id - string, youtube-id
    startTime - int, in ms
    endTime - int, in ms, set to 0 to view to end
  video             - Video to be shown in the background
    id                  - youtube-id
    startTime           - 0
    endTime             - 0
    service             - youtube

___EXAMPLE___
{
  'title': 'Quiz',
  'quizType': 'quiz',
  'type': 'quiz',
  'visibility': 0,
  'description': 'Made using quiztools.'
  'difficulty': 500,
  'audience': 'University',
  'language': 'English',

  'questions': 
  [{
    'question': u'What is the capital of Norway?',
    'points': True,
    'time': 60000,
    'numberOfAnswers': 4,
    'questionFormat': 0,
    'choices': 
    [{  
      'answer': u'Helsinki',
      'correct': False
    }, {
      'answer': u'Drammen',
      'correct': False
    }, {
      'answer': u'Oslo',
      'correct': True},
    }, {
      'answer': u'Denmark',
      'correct': False
    }],
    'video': 
    {
      'service': 'youtube',
      'endTime': 0,
      'id': '',
      'startTime': 0
    },
  }, {
    'question': u'Which of the following cities are capitals?',
    'points': True,
    'time': 60000,
    'numberOfAnswers': 4,
    'questionFormat': 0
    'choices': 
    [{
      'answer': u'Sidney',
      'correct': False
    }, {
      'answer': u'Kigali',
      'correct': True
    }, {
      'answer': u'Bonn',
      'correct': False
    }, {
      'answer': u'Bern',
      'correct': True
    }, {
      'answer': u'Ottawa',
      'correct': True
    }, {
      'answer': u'New York',
      'correct': False
    }],
    'video': 
    {
      'service': 'youtube',
      'endTime': 0,
      'id': '',
      'startTime': 0
    },
  }],
}
"""

class KahootQuizMaker(QuizMaker):
    """
    Uses the Kahoot service. Register a user at getkahoot.com. Accesses
    your quizzes manually at create.kahoot.it to edit or play them.
    """
    def __init__(self, user, force_new_token=False):
        self.user = user 

        # Get access token to be used in HTML requests
        self.__login(force_new_token)


    def __login(self, force_new_token=False):
        """Read access token from file or request new from server."""
        print "Getting access token... ",
        user = self.user
        try:
            assert force_new_token == False
            with open(".%s_kahoot_token.txt" % user, "r") as f:
                token = f.readline()
            print "sucsessfully read old token from file"

        except:
            print "failed to find token, generating new. "

            password = getpass.getpass("Enter password for Kahoot-user %s: "
                                       % user)

            # Kahoot login server
            url = "http://db.kahoot.it/rest/authenticate"

            # Dictionary with login data
            authparams = {"username": user,
                          "password": password,
                          "grant_type": "password"}

            r = requests.post(url, data=json.dumps(authparams),
                              headers={"content-type":"application/json"})

            # Assert HTML status of response
            r.raise_for_status()

            # Fetch token from response object
            token = r.json()[u"access_token"]

            # Write access token to a file for future use
            with open(".%s_kahoot_token.txt" % user, "w") as f:
                f.write(token)
            print "New access token recieved from server and saved to file."

        self.token = token

    def get_quiz(self, kahoot_id):
        """Fetch a given kahoot belonging to the user, returns dictionary."""
        vprint("Fetching given quiz from Kahoot... "),

        # URL for fetching specific kahoot
        url = "https://create.kahoot.it/rest/kahoots/%s" % kahoot_id

        r = requests.get(url, headers={
                         "content-type" : "application/json",
                         "authorization" : self.token})

        # Assert HTML status of response
        r.raise_for_status()
        vprint("success!")

        return r.json()

    def get_all_quizzes(self):
        """Fetch all kahoots belonging to user from server, return as list."""
        print "Fetching all quizzes from Kahoot... ",

        # URL for fetching all quizzes
        url = "https://create.kahoot.it/rest/kahoots/browse/private?limit=30"

        r = requests.get(url, headers={
                         "content-type" : "application/json",
                         "authorization" : self.token})

        # Assert HTML status of response
        r.raise_for_status()
        print "success!"
        return r.json()[u"entities"]

    def upload_quiz(self, quiz):
        """Upload a quiz (python dictionary) to Kahoot, return url and id."""
        print "Uploading quiz to kahoot... ",

        # URL for making quizzes
        url = "http://db.kahoot.it/rest/kahoots"

        r = requests.post(url, data=json.dumps(quiz), headers={
                                "content-type" : "application/json",
                                "authorization" : self.token})

        # Assert HTML status of response
        r.raise_for_status()
        
        print "success!"
        kahoot_id = r.json()["uuid"]
        return kahoot_id, self.fetch_url(kahoot_id)

    def fetch_url(self, kahoot_id):
        """Find url to access a certain quiz through a browser."""
        return r"https://play.kahoot.it/#/?quizId="+kahoot_id

    def delete_quiz(self, kahoot_id):
        """Delete kahoot of given id."""
        print "Deleting kahoot quiz... ",

        # URL for deleting specific kahoot
        url = "https://create.kahoot.it/rest/kahoots/%s" % kahoot_id

        # HTML delete request
        r = requests.delete(url, headers={
                                "content-type" : "application/json",
                                "authorization" : self.token})

        # Assert HTML status
        r.raise_for_status()
        print "success!"

    def delete_all_quizzes(self):
        """Delete all kahoots on a given user."""
        print "This will delete ALL your quizzes, are you sure? (Y/n)"
        if raw_input("...").lower() != "y":
            print "Aborting"
            return

        quizzes = self.get_all_quizzes()
        for q in quizzes:
            self.delete_quiz(q["uuid"])

        print "Done deleting kahoots. User should now be clean."

    def make_quiz(self, questions, **kwargs):
        """Take a list of dictionaries, return kahoot quiz dictionary."""
        print "Turning questions into a Kahoot quiz object."

        # Extract and modify questions
        for i, q in enumerate(questions):
            # Remove keys not relevant for Kahoot
            q.pop("no", None)
            q.pop("choice prefix", None)
            q.pop("question prefix", None)

            # Add choices
            for n, c in enumerate(q["choices"]):
                q["choices"][n] = {"answer" : c[1],
                    "correct" : c[0] == u"right"}

            # If there are more choices than 4, the rest are truncated
            if n+1 > 4:
                print "Warning: Kahoot only supports up to 4 answers, " \
                      "%i of the answers of question %i have been truncated!" \
                      % (n+1-4, i+1)

            # Additional question parameters
            q["numberOfAnswers"] = 4*(n+1 > 4) + (n+1)*(n+1 <= 4)
            q["questionFormat"] = 0
            q["time"] = 60000
            q["video"] = {"id" : "",
                          "startTime" : 0,
                          "endTime" : 0,
                          "service" : "youtube"}
            q["points"] = True

        # Add additional parameters
        # Default parameters
        quiz = {
                 "title" : "Quiz",
                 "questions" : questions,
                 "quizType": "quiz",
                 "visibility": 0,  # 0: private, 1: public
                 "type": "quiz",
                 "difficulty": 500,
                 "audience": "University",
                 "language": "English",
                 "description": "Made using quiztools."
                }

        # User-given parameters
        for key in kwargs:
            if key == "cover":
                url = self.upload_image(kwargs["cover"])
                quiz["cover"] = url
            else:
                quiz[key] = kwargs[key]

        return quiz

    def upload_image(self, img_filename):
        """Take image filename, post image to kahoot server, return url."""
        print "Uploading image to server... ",

        with open(img_filename, "rb") as img:
            # URL for uploading media
            url = "https://create.kahoot.it/media-api/media/upload"

            img_type = img_filename.split(".")[-1]
            if img_type not in ["gif", "jpg", "png", "jpeg"]:
                print "Error: %s is not a supported file-type for Kahoot."
                print "Make sure image file is png, jpg, jpeg or gif."
                print "Image has not been uploaded."
                return ""

            files = {"f": (img_filename, img, "image/%s" % img_type)}

            r = requests.post(url, files=files, headers=
                             {"authorization" : self.token})

        # Assert HTML status
        r.raise_for_status()

        print "success!"

        return r.json()["uri"]


"""
___JotForm syntax guide___

The "form" object is used as input to upload_quiz, and as output from
get_quiz and get_quizzes with JotFormQuizMaker. It is a python dictionary
with two keys: "properties" and "questions". The value of both
keys should be dictionaries. The properties is a set of key:value 
parameters, the questions is a dictionary where the keys are "1",
"2", etc. The value of these keys are again dictionaries where
the key:value pairs are the question parameters. Note that elements such as
headers and submit-buttons are also included in the questions-dictionary. 

___PARAMETERS___ (All params must be given as strings)
properties
  title - the title of the form
  font  - "Lucia Grande" is default, "Courier" is monospace
questions
  name - has no influence, but needs to be set
  order - in which order the elements are shown in the form
  special - predefined collections such as gender/date etc, set to "None"
  type - what type of element it is control_radio/control_head/control_button
  text - text of header/question etc.
  subHeader - sub-title, only relevant for headers
  spreadCols - the number of columns used to show the choices
  required - is the question mandatory? "Yes/No"
  options - choices, should be given as one string with options seperated by |
  labelAlign - where question text is located, "Top"/"Left"/"Right"/"Auto"
  buttonAlign - where button is located
  allowOther - allow free-text "Other" answer, "Yes/No"
  otherText - default other text, only relevant if allowOther is Yes

These parameters are sufficient to create a functional form on JotForm.
For a more complete list, you can pull a pre-existing form from your JotForm 
user with JotFormQuizMaker.get_quiz and examine the resulting form-object.

___EXAMPLE___
{
  'properties': 
  {
    'title': 'Quiztools test quiz!',
    'font': 'Courier',
    'styles': 'nova'
  },

  'questions': 
  {
    # Title header
    '1':
    { 
      'headerType': u'Large',
      'name': u'titleHeader',
      'order': '1',
      'type': 'control_head',
      'text': 'Quiztools test quiz!',
      'subHeader': 'Made using QuizMaker'
    },
    # Multiple choice question using radio buttons
    '2':
    {
      'name': 'firstQuestion',
      'order': '2',
      'special': 'None',
      'type': 'control_radio',
      'text': 'What is the capital of Norway?',
      'spreadCols': '1', # Displays options nder each other
      'reqired': 'No',
      'options': 'Sydney|Oslo|Stockholm|Paris|Keflavik',
      'labelAlign': 'Top',
      'allowOther': 'No',
      'otherText': 'Other'             
    },
    '3':
    {
      'name': 'submitButton',
      'type': 'control_buttom'
      'buttonAlign': 'Auto',
      'order': 3,
      'clear': 'No',
      'print': 'No',
      'text': 'Submit',
      'buttonStyle': 'simple_white'
    }
  }
}
"""

class JotformQuizMaker(QuizMaker):
    """
    Uses the Jotform service. Register a user at jotform.com.
    Get the python 2.7 API from https://github.com/jotform/jotform-api-python
    Get an API key from http://www.jotform.com/myaccount/api.
    """
    def __init__(self, user, new_api_key=False):
        self.user = user
        # Creates an API client using the API key
        self.__login(new_api_key)

    def __login(self, new_api_key=False):
        """Read API key from file or request one from user, create API-client."""
        from jotform import JotformAPIClient
        print "Creating client... ",
        user = self.user
        try:
            assert (new_api_key==False)
            with open(".%s_jotform_API_key.txt" % user, "r") as f:
                api_key = f.readline()
            print "sucsessfully read API key from file"

        except:
            print "failed to find API key. Please generate one at http://www." \
                  "jotform.com/myaccount/api and paste it here."
            api_key = raw_input("API_key: ")

            # Write API key to file for future use
            with open(".%s_jotform_API_key.txt" % user, "w") as f:
                f.write(api_key)
            print "API key has been saved to file for future use."

        self.client = JotformAPIClient(api_key, debug=True)

    def upload_quiz(self, form):
        """
        Take a JotForm form-object and upload it, return the id assigned
        to the form and the url where it can be located.
        For more information on the JotForm form-object, see the JotForm 
        syntax guide.
        """
        print "Uploading quiz to JotForm... ",

        # Uses the JotForm API
        r = self.client.create_form(form)
        
        return r['id'], r['url']

    def get_quiz(self, form_id):
        """Fetch a given quiz belonging to the user, returns dictionary."""
        print "Fetching given quiz from JotForm...",

        # Note: client.get_form() only gets basic information about a form

        properties = self.client.get_form_properties(form_id)
        questions = self.client.get_form_questions(form_id)

        print "success!"

        return {"properties" : properties, "questions" : questions}

    def get_all_quizzes(self):
        """Fetch all forms belonging to user from server, return as list."""
        print "Fetching all quizzes from JotForm... ",

        # Note, client.get_forms() only returns basic information about forms
        quizzes = [self.get_quiz(f[u'id']) for f in self.client.get_forms()]

        print "success!"
        return quizzes

    def delete_quiz(self, quiz_id):
        """Delete form of given id."""
        print "Deleting JotForm form... ",
        self.client.delete(quiz_id)
        print "success!"

if __name__ == "__main__":
    '''
    #### EXAMPLES USING Kahoot
    # Create QuizMaker-object
    qm = KahootQuizMaker("jvbrink")

    # Example of reading .quiz file, then making and uploading a kahoot quiz
    questions = qm.read_quiz_file("../demo-quiz/.test_jonas.quiz")
    quiz = qm.make_quiz(questions) #, cover="../demo-quiz/fig/red_panda.jpg")
    kahoot_id, url = qm.upload_quiz(quiz)

    # Example of fetching a pre-existing Kahoot
    #q = qm.get_all_quizzes()
    #kahoot_id =  q[0]["uuid"]
    #quiz = qm.get_quiz(kahoot_id)

    # Deleting all quizzes on users Kahoot page
    # qm.delete_all_quizzes()
    '''

    #### EXAMPLES USING JOTFORM
    # Create QuizMaker-object
    qm = JotformQuizMaker("jvbrink")
    
    