"""
Uses the python pacakge requests, see
http://docs.python-requests.org/en/latest/
"""

import json
import requests
import HTMLParser
import getpass

class QuizMaker:
    """Base class for quiz makers."""
    def _login(self, user, password):
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

# HPL: Can you format the kahoot_quiz_syntax file to fit in here
# as a triple-quoted string? It's good to have the syntax definition
# right here along with the implementation.

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
        print "Fetching given quiz from Kahoot... ",

        # URL for fetching specific kahoot
        url = "https://create.kahoot.it/rest/kahoots/%s" % kahoot_id

        r = requests.get(url, headers={
                         "content-type" : "application/json",
                         "authorization" : self.token})

        # Assert HTML status of response
        r.raise_for_status()
        print "success!"

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
        """Upload a quiz (python dictionary) to Kahoot."""
        print "Uploading quiz to kahoot... ",

        # URL for making quizzes
        url = "http://db.kahoot.it/rest/kahoots"

        r = requests.post(url, data=json.dumps(quiz), headers={
                                "content-type" : "application/json",
                                "authorization" : self.token})

        # Assert HTML status of response
        r.raise_for_status()
        print "success!"


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


if __name__ == "__main__":
    #### EXAMPLES USING Kahoot
    # Create QuizMaker-object
    qm = KahootQuizMaker("jvbrink")

    # Example of reading .quiz file, then making and uploading a kahoot quiz
    questions = qm.read_quiz_file("../demo-quiz/.test_jonas.quiz")
    quiz = qm.make_quiz(questions) #, cover="../demo-quiz/fig/red_panda.jpg")
    qm.upload_quiz(quiz)

    # Example of fetching a pre-existing Kahoot
    #q = qm.get_all_quizzes()
    #kahoot_id =  q[0]["uuid"]
    #quiz = qm.get_quiz(kahoot_id)

    # Deleting all quizzes on users Kahoot page
    # qm.delete_all_quizzes()

    """
    #### EXAMPLES USING JOTFORM
    # Create QuizMaker-object
    qm = JotformQuizMaker("jvbrink")
    """
