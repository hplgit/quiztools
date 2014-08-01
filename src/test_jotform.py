from jotform import *

api_key = '8b03bc70c8f88d73b36c693def767651'
client = JotformAPIClient(api_key, debug=True)

def read_quiz_file(quiz_file):
        """Read a .quiz file, return a list of dictionaries."""
        print "Reading .quiz-file... ",
        with open(quiz_file) as f:
            questions = eval(f.read())
        assert type(questions) == list
        assert type(questions[0]) == dict
        print "success!"
        return questions

questions = read_quiz_file("../demo-quiz/.test_jonas.quiz")


pattern = r'''<img +src=["'](.+?)["']'''
import re
filenames = re.findall(pattern, html_text)
for filename in filenames:
   # upload filename

form = \
{
    'properties':
    {
        u'stopHighlight': u'Yes',
        u'defaultEmailAssigned': u'No',
        u'pagetitle': u'Form',
        'title': 'Apple',
        'injectCSS': '.form-all {\nborder: 1px solid;\n}',
        u'thanktext': u'Your scored {score}&amp;nbsp;out of 5 on the quiz\n{form_title}\n&amp;nbsp;\n',
        'sendpostdata': 'No',
        'activeRedirect': 'thanktext'
    },
    'questions': {}
}

# u'emails': [{u'body': u'\n    \n    \n      &amp;nbsp;\n    \n    \n      \n        \n          \n          \n          \n        \n      \n      \n        \n          \n          \n\nQuestion\nAnswer\n\n\nWhat is the capital of Norway?{2}\n\nWhich of the following cities are capitals?{3}\n\nScore{score}\n\n          \n          \n        \n        \n          \n          \n          \n        \n      \n    \n    \n      &amp;nbsp;\n    \n  ',
# u'from': u'default', u'name': u'Notification', u'to': u'jonasvdbrink@gmail.com', u'html': u'1', u'type': u'notification', u'subject': u'New submission: {form_title}'}], u'expireDate': u'No Limit',
# u'thanktext': u'Your scored {score}&amp;nbsp;out of 5 on the quiz\n{form_title}\n&amp;nbsp;\n{pdf-link}',
# u'optioncolor': u'#000', u'sendpostdata': u'No', u'formWidth': u'650'}



# Add header to the quiz
form['questions']['1'] = \
{
    'headerType': 'Large',
    'name': 'titleHeader',
    'order': '1',
    'type': 'control_head',
    'text': 'Quiztools test quiz!',
    'subHeader': 'Complete the quiz to check your score',
    'activeRedirect': 'thanktext'}

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
    question[u'calcValues'] = "|".join([str(1*(c[0]=='right')) 
                              for c in q["choices"]])
    form['questions'][str(len(form['questions'])+1)] = question

# Add a hidden score tab
form['questions'][str(len(form['questions'])+1)] = \
{
    'name': 'score',
    'required': 'no',
    'text': 'Score',
    'defaultResult': '0',
    'hidden': 'Yes',
    'size': 20,
    'type': 'control_calculation',
    'order': str(len(form['questions'])+1)
}

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

# Add properties used in calculation
eq = "+".join(['{%i}' % i for i in range(2,len(form['questions'])-1)])

#form["properties"]["calculations"] = [{'equation': ('[' + eq + ']')}]


# u'calculations': 
#  [{
#     u'showEmptyDecimals': u'',
#     u'operands': u'2,5',
#     u'equation': u'[{2}+{5}]',
#     u'newCalculationType': u'1',
#     u'showBeforeInput': u'',
#     u'insertAsText': u'',
#     u'readOnly': u'1',
#     u'decimalPlaces': u'2',
#     u'resultField': u'3',
#     u'ignoreHiddenFields': u''}],
 
# "1" + ","*(len(form["questions"])-4)
# form["properties"]["equation"] = \

r = client.create_form(form)
qid = r['id']

#for f in client.get_forms():
#  print f['title'], f['id']

#qid = "41912233206343"

#client.set_form_properties(qid, {'sendpostdata': 'No'})
#print client.get_form_questions(qid)

#print r['url']
'''

qid = '41911951941355'

print client.get_form_properties(qid)
'''