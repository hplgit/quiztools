#!/usr/bin/env python
import quiztools.KahootQuizMaker
import logging

def main():
    import sys
    # Merge several .quiz files in the current directory,
    # given on the command line
    if len(sys.argv) < 4:
        print 'Usage: quiztools-main.py user "Title of Quiz" .my.quiz .your.quiz ...'
        sys.exit(1)

    user = sys.argv[1]
    title = sys.argv[2]
    qm = quiztools.KahootQuizMaker.KahootQuizMaker(
        user, path='', loglvl=logging.INFO)
    questions = []
    for filename in sys.argv[3:]:
        if not os.path.isfile(filename):
            print 'File %s does not exist!' % filename
            sys.exit(1)
        questions += qm.read_quiz_file(filename)

    quiz = qm.make_quiz(questions, title=title)

    kahoot_id, url = qm.upload_quiz(quiz)

    print "\n\n\nUploaded quiz can be viewed at %s" % url

def delete_all_quizzes():
    # Better to import module and run the statements manually
    import sys
    user = sys.argv[1]
    qm = quiztools.KahootQuizMaker.KahootQuizMaker(
        user, path='', loglvl=logging.INFO)
    # Deleting all quizzes on user's Kahoot page
    qm.delete_all_quizzes()

main()
