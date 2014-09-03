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
from QuizMaker import QuizMaker

"""
___JotForm syntax guide___

The 'form' object is used as input to upload_quiz, and as output from
get_quiz and get_quizzes with JotFormQuizMaker. It is a python dictionary
with two keys: 'properties' and 'questions'. The value of both
keys should be dictionaries. The properties is a set of key:value 
parameters, the questions is a dictionary where the keys are '1',
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
            'headerType': 'Large',
            'name': 'titleHeader',
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
    def __init__(self, user, force_new=False):
        self.user = user
        # Creates an API client using the API key
        self.login(force_new)

    def login(self, force_new=False):
        """Read API key from file or request one from user, create API-client."""
        from jotform import JotformAPIClient
        print "Creating client... ",
        user = self.user
        try:
            assert (force_new==False)
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
        
        print "success!"
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
        form_filter = {"status:ne":"DELETED"}
        forms = self.client.get_forms(None, None, form_filter, None)
        quizzes = [self.get_quiz(f[u'id']) for f in forms]

        print "success!"
        return quizzes

    def delete_quiz(self, quiz_id):
        """Delete form of given id."""
        print "Deleting JotForm form... ",
        self.client.delete_form(quiz_id)
        print "success!"

    def delete_all_quizzes(self):
        """Delete all forms of user."""
        print "Deleting all JotForm forms... ",
        for quiz_id in [f[u'id'] for f in self.client.get_forms()]:
            self.delete_quiz(quiz_id)
        print "success!"

    def make_quiz(self, questions, **kwargs):
        """
        Take a list of dictionaries of the format given by reading 
        a .quiz-file. Return the corresponding JotForm quiz-object.
        """
        print "Turning questions into a JotForm quiz-object."

        form = \
        {
            'properties':
            {
                'title': 'Quiztools test quiz!',
                #'sendpostdata': u'No',
                #'activeRedirect': u'thanktext'
            },
            'questions': {}
        }
       
        # Add form properties
        for k in kwargs:
          form['properties'][k] = kwargs[k]

        # Add header to the quiz
        form['questions']['1'] = \
        {
            'headerType': 'Large',
            'name': 'titleHeader',
            'order': '1',
            'type': 'control_head',
            'text': 'Quiztools test quiz!',
            'subHeader': 'Made using quiztools',
        }
        
        default_question = \
        {
            'name': '',
            'special': 'None',
            'spreadCols': '1',
            'required': 'No',
            'labelAlign': 'Top',
            'allowOther': 'No',
            'otherTest': 'Other',
        }

        for q in questions:
            question = default_question.copy()
            question['name'] = str(len(form['questions'])+1)
            question['text'] = q['question']
            question['order'] = str(len(form['questions'])+1)
            question['options'] = "|".join(c[1] for c in q['choices'])
            #nc = sum([c[0]=='right' for c in q['choices']])
            question['type'] = 'control_radio' #if (nc == 1) \
                                           #else 'control_checkbox'
            question['calcVales'] = "|".join([str(1*(c[0]=='right')) 
                                      for c in q["choices"]])
            form['questions'][str(len(form['questions'])+1)] = question


        # Add a submit button to quiz
        form['questions'][str(len(form['questions'])+1)] = \
        {
            'name': 'submitButton',
            'type': 'control_button',
            'buttonAlign': 'Auto',
            'order': str(len(form['questions'])+1),
            'clear': 'No',
            'print': 'No',
            'text': 'Complete Quiz',
            'buttonStyle': 'simple_blue'
        }

        return form
