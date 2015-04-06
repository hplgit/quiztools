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

    def make_quiz(self, questions, **kwargs):
        """
        Take a list of dictionaries as found when parsing .quiz-file,
        return a quiz-object specialized for the given website.
        """
        raise NotImplementedError

    @staticmethod
    def read_quiz_file(filename):
        """Read a .quiz file, return a list of dictionaries."""
        logging.info("Parsing .quiz-file.")
        with open(filename) as f:
            questions = eval(f.read())
        try:
            assert type(questions) == list
            assert type(questions[0]) == dict
            logging.info("File succesfully parsed.")
            return questions
        except:
            logging.error("Format of file %s not understood." % filename)
            return 

    @staticmethod
    def find_images(html_text):
        """Parse a HTML string and return list of image filenames."""
        pattern = r'''<img +src=["'](.+?)["']'''
        img_filenames = re.findall(pattern, html_text)
        return img_filenames
    
    @staticmethod
    def find_math(html_text):
        """Check if a HMTL string contains math and return boolean."""
        patterns = [r'\\\( .*? \\\)', r'\$\$']
        for pattern in patterns:
            if re.search(pattern, html_text):
                return True
        return False

    @staticmethod
    def find_code(html_text):
        """Check if a HMTL string contains math and return boolean."""
        patterns = ['<pre', '<code>']
        for pattern in patterns:
            if re.search(pattern, html_text):
                return True
        return False
