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

class QuizMaker:
    """Base class for quiz makers."""
    def login(self, force_new=False, loglvl=logging.warning):
        """Get access to given site."""
        raise NotImplementedError

    def get_quiz(self, quiz_id):
        """Return quiz-object with given id."""
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
        logging.info("Parsing .quiz-file.")
        with open(self.path+quiz_file) as f:
            questions = eval(f.read())
        assert type(questions) == list
        assert type(questions[0]) == dict
        logging.info("File succesfully parsed.")
        return questions

    def make_quiz(self, questions, **kwargs):
        """Take a list of dictionaries as found when parsing .quiz-file,
        return a quiz-object specialized for the given website."""
        raise NotImplementedError

    def find_images(self, html_text):
        """Parse a HTML string and extract image filenames."""
        pattern = r'''<img +src=["'](.+?)["']'''
        img_filenames = re.findall(pattern, html_text)
        return img_filenames