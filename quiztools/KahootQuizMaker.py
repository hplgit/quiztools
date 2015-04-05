# -*- coding: utf-8 -*-

"""
Uses the python pacakge requests, see
http://docs.python-requests.org/en/latest/
"""

import json
import requests
import getpass
import re
import sys
import logging
import random
from QuizMaker import QuizMaker

"""
___Kahoot syntax guide___

The 'quiz' object is used as input to upload_quiz, and as output from
get_quiz and get_quizzes with KahootQuizMaker. It is a python dictionary
with various key:value parameters. One of these keys are 'questions', which
should be a list of dictionaries corresponding to each question.

___PARAMETERS___
title - string, title of the quiz
type - string, not in use, set it to 'quiz
'quizType - string, 'quiz'/'poll'/'survey'
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
    questionFormat - int, 0 for image, 1 for video, 2 for iframe
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
        service - "youtube", only supported service so feature

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
            'correct': True
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
    def __init__(self, user, path="", force_new=False, loglvl=logging.WARNING):
        self.user = user
        self.path = path
        logging.basicConfig(format='%(message)s', level=loglvl)

        # Get access token to be used in HTML requests
        self.login(force_new)


    def login(self, force_new=False):
        """Read access token from file or request new from server."""
        logging.info("Setting up access token."),
        user = self.user

        try:
            assert force_new == False
            with open(".%s_kahoot_token.txt" % user, "r") as f:
                self.token = f.readline()
            logging.info("Old token was sucsessfully read from file.")

        except:
            logging.info("Requesting a new access token from Kahoot Servers.")
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
            self.token = r.json()[u"access_token"]

            # Write access token to a file for future use
            with open(".%s_kahoot_token.txt" % user, "w") as f:
                f.write(self.token)
            logging.info("New token recieved from server and saved to file.")

        # Assert that connection works
        try:
            self.get_all_quizzes()
        except:
            # If connection fails, it may be to an outdated access token
            if force_new == False:
                logging.warning("Access denied. Token may be outdated." \
                                "Requesting new token from server.")
                self.login(force_new=True)
            if force_new == True:
                logging.error("Access denied.")

    def get_quiz(self, kahoot_id):
        """Fetch a given kahoot belonging to the user, returns dictionary."""
        logging.info("Fetching quiz %d from Kahoot servers." % kahoot_id),

        # URL for fetching specific kahoot
        url = "https://create.kahoot.it/rest/kahoots/%s" % kahoot_id

        r = requests.get(url, headers={
                         "content-type" : "application/json",
                         "authorization" : self.token})

        # Assert HTML status of response
        r.raise_for_status()
        logging.info("Quiz was fetched sucsessfully.")
        return r.json()

    def get_all_quizzes(self):
        """Fetch all kahoots belonging to user from server, return as list."""
        logging.info("Fetching all your quizzes from Kahoot servers.")

        # URL for fetching all quizzes
        url = "https://create.kahoot.it/rest/kahoots/browse/private?limit=30"

        r = requests.get(url, headers={
                         "content-type" : "application/json",
                         "authorization" : self.token})

        # Assert HTML status of response
        r.raise_for_status()
        logging.info("All quizzes returned successfully.")
        return r.json()[u"entities"]

    def upload_quiz(self, quiz):
        """Upload a quiz (python dictionary) to Kahoot, return url and id."""
        logging.info("Uploading quiz to kahoot.")

        # URL for making quizzes
        url = "http://db.kahoot.it/rest/kahoots"

        r = requests.post(url, data=json.dumps(quiz), headers={
                                "content-type" : "application/json",
                                "authorization" : self.token})

        # Assert HTML status of response
        r.raise_for_status()

        logging.info("Quiz successfully uploaded.")
        kahoot_id = r.json()["uuid"]
        return kahoot_id, self.fetch_url(kahoot_id)

    def fetch_url(self, kahoot_id):
        """Find url to access a certain quiz through a browser."""
        return r"https://play.kahoot.it/#/?quizId="+kahoot_id

    def delete_quiz(self, kahoot_id):
        """Delete kahoot of given id."""
        logging.info("Deleting quiz %s from Kahoot servers." % kahoot_id)

        # URL for deleting specific kahoot
        url = "https://create.kahoot.it/rest/kahoots/%s" % kahoot_id

        # HTML delete request
        r = requests.delete(url, headers={
                                "content-type" : "application/json",
                                "authorization" : self.token})

        # Assert HTML status
        r.raise_for_status()
        logging.info("Quiz successfully deleted.")

    def delete_all_quizzes(self):
        """Delete all kahoots on a given user."""
        print "This will delete ALL your quizzes, are you sure? (Y/n)"
        if raw_input("...").lower() != "y":
            logging.warning("Deletion aborted.")
            return

        quizzes = self.get_all_quizzes()
        for q in quizzes:
            self.delete_quiz(q["uuid"])

        logging.info("Kahoots deleted from user. User should now be clean.")


    def make_quiz(self, questions, quiz_format='modern', shuffle_answers=True, default_time=60000, **quizargs):
        """
        Take a list of dictionaries, return kahoot quiz dictionary.

        Arguments:
        questions - Dictionary of questions, such as made by make_quiz
        shuffle_answers - shuffles the order the answers are shown
        default_time - The default time of each question
        quizformat - Choose 'classic' for normal Kahoot-formatting, 'modern' for code/math
        quizargs - Changes the quiz parameters, such as title, visibility, etc.
        """
        logging.info("Turning questions into a Kahoot quiz object.")

        if quiz_format != 'modern' and quiz_format != 'classic':
            logging.warning("Value of quiz_format not understood. Valid values are 'modern'/'classic', using modern.")
            modern = True

        # Parse over all questions
        for q_nr, q in enumerate(questions):

            # Remove keys not relevant for Kahoot
            q.pop("no", None)
            q.pop("choice prefix", None)
            q.pop("question prefix", None)

            # Check number of answers
            if len(q["choices"]) > 4:
                logging.warning("Warning: Kahoot only supports up to 4 answers"\
                ", %i of the answers of question %i have been truncated." \
                % (len(q["choices"])-4, q_nr+1))

                # Make sure we don't truncate all the correct answers
                # Choose at least 1 correct answer and fill up with wrong ones
                if shuffle_answers: random.shuffle(q["choices"])
                q["choices"].sort(key=lambda c: c[0]==u'wrong')
                choices = q["choices"][:3]
                choices.append(q["choices"][-1])
                random.shuffle(choices)
            else:
                choices = q["choices"]
                if shuffle_answers: random.shuffle(choices)

            # Check answers for images and mark-up
            answers_markup = False
            for c in choices:
                image = QuizMaker.find_images(c[1])
                if image:
                    logging.warning("Question %i has an image in one" /
                    "of the answers, this is not supported by Kahoot. The"/
                    " image will be ignored." % (q_nr+1))
                    c[1] = re.sub('<.*?>', '', q["question"])

                math = QuizMaker.find_math(c[1])
                code = QuizMaker.find_code(c[1])
                if math or code:
                    answers_markup = True

            if quiz_format == 'classic':
                q["choices"] = []
                for c in choices:
                    q["choices"].append({"answer" : c[1],
                        "correct" : c[0] == u"right"})
                q["numberOfAnswers"] = len(choices)
            elif quiz_format == 'modern':
                # Use empty choices-fields as answers are moved into iframe
                letters = ['a)', 'b)', 'c)', 'd)']
                q["choices"] = []
                for j, c in enumerate(choices):
                    q["choices"].append({"answer" : letters[j],
                                        "correct" : c[0] == u'right'})
                q["numberOfAnswers"] = len(choices)

            # Check question for images and mark-up
            images = QuizMaker.find_images(q["question"])
            math = QuizMaker.find_math(q["question"])
            code = QuizMaker.find_code(q["question"])
            question_markup = math or code
            markup = question_markup or answers_markup

            if quiz_format == 'classic':
                logging.info("Generating a 'classic'-style quiz.")

                # Check for incompatibility
                if markup:
                    logging.error("The given quiz contains code and/or math markup"/
                    " but uses the classic quiz_format, which does not support markup.")
                    raise AssertionError

                # Check for too many images
                if len(images) > 1:
                    logging.warning("Warning: Question %i contains several"/
                    "images, but Kahoot only supports up to one image per "/
                    "question. The additional images will be ignored." % (q_nr+1))
                    images = [images[0]]

                q["question"] = re.sub('<.*?>', '', q["question"])
                q["image"] = self.upload_image(images[0])
                q["questionFormat"] = 0 # Image format

            elif quiz_format == 'modern':
                logging.info("Generating a 'modern'-style quiz.")

                # Check for incompatibility
                if images:
                    logging.warning("The quiz format chosen is 'modern', which"/
                    "does not support images. All images in the quiz will be ignored.")
                    q["question"] = re.sub('<.*?>', '', q["question"])
                    images = []

                iframe_str = self.iframe_str(q["question"], choices)
                q["iframe"] = {"content" : iframe_str}
                q["question"] = ""
                q["questionFormat"] = 2  # iframe format
                q["image"] = ""

            # Additional question parameters
            q["time"] = default_time
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
        for key in quizargs:
            if key == "cover":
                url = self.upload_image(quizargs["cover"])
                quiz["cover"] = url

            else:
                quiz[key] = quizargs[key]

        logging.info("Quiz-object successfully made.")
        return quiz

    def style(self):
        """Defines the CSS style to be used in the iframe."""
        style = """
                <style>
                    body {font-family:sans-serif;
                          font-size:14pt;}
                    .question {font-size:22pt;
                               font-weight:bold;}
                    .answer {}
                    .letter {font-weight:bold;}
                </style>
                """
        return style

    def script(self):
        """Defines the script to be run in the iframe setup."""
        script = """<script type="text/x-mathjax-config">
                    MathJax.Hub.Config({
                      TeX: {
                         equationNumbers: {  autoNumber: "AMS"  },
                         extensions: ["AMSmath.js", "AMSsymbols.js", "autobold.js", "color.js"]
                      }
                    });
                    </script>
                    <script type="text/javascript"
                     src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
                    </script>"""
        script = """<script type='text/javascript' src='//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>"""
        return script


    def iframe_str(self, question, choices):
        """Take question text and list of choices return the iframe string."""
        head = "<html><head>%s%s</head>" % (self.style(), self.script())
        body = "<body><p class='question'>%s</p>" % question

        letters = ["<span class='letter'>%s)</span>" % l
                                                    for l in 'a','b','c','d']
        for i, choice in enumerate(choices):
            body += "<hr>"
            body += "<p class='answer'>%s %s</p>" % (letters[i], choice[1])
            if i==3: break
        body += "</body></html>"

        return head+body

    def upload_image(self, img_filename):
        """Take image filename, post image to kahoot server, return url."""
        logging.info("Uploading image to server.")

        with open(self.path+img_filename, "rb") as img:
            # URL for uploading media
            url = "https://create.kahoot.it/media-api/media/upload"

            img_type = img_filename.split(".")[-1]
            if img_type not in ["gif", "jpg", "png", "jpeg"]:
                logging.error("%s isn't a supported file-type for Kahoot.")
                logging.error("Make sure image file is png, jpg, jpeg or gif.")
                logging.error("Image has not been uploaded.")
                return ""

            files = {"f": (img_filename, img, "image/%s" % img_type)}
            r = requests.post(url, files=files, headers=
                             {"authorization" : self.token})

        # Assert HTML status
        r.raise_for_status()
        logging.info("Image successfully uploaded to kahoot server.")
        return r.json()["uri"]

    def read_quiz_file(self, filename):
        """Read a .quiz file, return a list of dictionaries."""
        return QuizMaker.read_quiz_file(self.path+filename)


def tester(tester='jonas'):
    if tester == 'jonas':
        # Create QuizMaker-object
        qm = KahootQuizMaker("jvbrink", path="../demo-quiz/", loglvl=logging.INFO)

        # Example of reading .quiz file, then making and uploading a kahoot quiz
        questions = qm.read_quiz_file(".sample_quiz.quiz")
        quiz = qm.make_quiz(questions, quiz_format='modern', default_time=60000, visibility=1, title='Sample Quiz!')

        kahoot_id, url = qm.upload_quiz(quiz)
        print "\n\n\nUploaded quiz can be viewed at %s" % url

        # Deleting all quizzes on users Kahoot page
        #qm.delete_all_quizzes()

    elif tester == 'hpl':
        qm = KahootQuizMaker("hplgame", path="../../INF1100-quiz/summerjob14/", loglvl=logging.INFO)

        questions = qm.read_quiz_file(".looplist_2.quiz")
        quiz = qm.make_quiz(questions, title='Loops and lists')

        kahoot_id, url = qm.upload_quiz(quiz)

        print "\n\n\nUploaded quiz can be viewed at %s" % url

        # Deleting all quizzes on users Kahoot page
        #qm.delete_all_quizzes()


if __name__ == "__main__":
    tester()
