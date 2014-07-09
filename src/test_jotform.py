from jotform import *

api_key = '8b03bc70c8f88d73b36c693def767651'
client = JotformAPIClient(api_key, debug=True)

form = {
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
      'type': 'control_button',
      'buttonAlign': 'Auto',
      'order': 3,
      'clear': 'No',
      'print': 'No',
      'text': 'Submit',
      'buttonStyle': 'simple_white'
    }
  }
}
'''
{
    },
    'questions':
    {
        u'1': 
        {
            u'name': u'T',
            u'allowOther': u'No',
            u'required': u'No',
            u'spreadCols': u'1',
            u'options': u'Oslo|Island|Stockholm|Paris|Keflavik|Bueno Aires',
            u'text': u'What is the capital of Norway?',
            u'qid': u'1',
            u'otherText': u'Other',
            u'type': u'control_radio',
            u'order': u'2',
            u'special': u'None',
            u'labelAlign': u'Top'
        },
        u'2': 
        {   
            u'subHeader': u'Made using quiztools',
            u'headerType': u'Large',
            u'qid': u'2',
            u'text': u'Quiz',
            u'type': u'control_head',
            u'order': u'1',
            u'name': u'clickTo'
        }
    }
}
'''

response = client.create_form(form)
print response['url']
print response['id']

# client.set_debugMode(False)

#for qid in [form[u'id'] for form in client.get_forms()]:
#    print client.get_form_questions(qid)

# print quiz_id



#form = client.get_form_questions(quiz_id)

#print form        


'''
__Jotform Syntax__
The form object is a dictionary with two keys,
"properties" and "questions". The value corresponding
to both keys should be dictionaries, "properties" has
key:value pairs where each key is a parameter. While
"questions" has integer keys, one for each element 
in the form. Each multiple-choice question will be such
an element, but headers and a submit button will also be.
A list of parameters follow

Properties
    title - str, title of the form
    styles - str, predefined styles, default is "nova" see webpage for more
    font - str, default is "Lucia Grande", "Courier" is monospace
    formString - dict, a dictionary of strings to be printed in different scenarios.
    showProgressBar - ('Enabled/'disable') 
    highlightLine - (u'Enabled')
        

Question parameters
    name        # ???
    order       # Order in the form
    qid         # ???
    special     # Collection of predefined values to be used on your form, such as gender/date etc., set to "None".
    type        # control_radio/control_head
    text        # Text of header/question etc.
    subHeader   # Sub-title, relevant for headers
    spreadCols  # How many columns should the choices be spread out in? 
    required    # Is the question mandatory? "Yes/No"
    options     # Answer choices, should be given as string in following manner u'Oslo|Island|Stockholm'
    labelAlign  # Where question text is located, Top/Left/Right/Auto

    allowOther  # Allow free-text "Other" answer "Yes/No"
    otherText   # Default other text, only relevant if allowOther is Yes
'''



{
    'properties': 
    {
        u'lineSpacing': u'12',
        u'defaultEmailAssigned': u'Yes',
        u'pagetitle': u'Form',
        u'messageOfLimitedForm': u'This form is currently unavailable!',
        u'hideMailEmptyFields': u'disable', 
        u'font': u'Lucida Grande', 
        u'id': u'41884371899372', 
        u'alignment': u'Left', 
        u'activeRedirect': u'default', 
        u'uniqueField': u'', 
        u'showProgressBar': u'disable', 
        u'limitSubmission': u'No Limit', 
        u'fontcolor': u'#555', 
        u'styles': u'nova', 
        u'hash': u'8z6j16t1ws', 
        u'formStrings': 
        {  
            u'submissionLimit': u'Sorry! Only one entry is allowed.  Multiple submissions are disabled for this form.',
            u'required': u'This field is required.',
             u'uploadFilesize': u'File size cannot be bigger than:',
             u'requireEveryRow': u'Every row is required.',
             u'uploadExtensions': u'You can only upload following files:',
             u'pleaseWait': u'Please wait...',
             u'gradingScoreError': u'Score total should only be less than or equal to',
             u'numeric': u'This field can only contain numeric values',
             u'inputCarretErrorA': u'Input should not be less than the minimum value:',
             u'alphanumeric': u'This field can only contain letters and numbers.',
             u'lessThan': u'Your score should be less than or equal to',
             u'incompleteFields': u'There are incomplete required fields. Please complete them.',
             u'confirmEmail': u'E-mail does not match',
             u'confirmClearForm': u'Are you sure you want to clear the form?',
             u'requireOne': u'At least one field required.',
             u'alphabetic': u'This field can only contain letters',
             u'maxDigitsError': u'The maximum digits allowed is',
             u'email': u'Enter a valid e-mail address',
             u'inputCarretErrorB': u'Input should not be greater than the maximum value:'
        },
        u'highlightLine': u'Enabled',
        u'fontsize': u'14',
        u'labelWidth': u'150',
        u'unique': u'None',
        u'emails': 
        [{
            u'body': u'\n    \n    \n      &amp;nbsp;\n    \n    \n      \n        \n          \n          \n          \n        \n      \n      \n        \n          \n          \n\nQuestion\nAnswer\n\n\nWhat is the capital of Norway?{whatIs}\n\n{clickTo3}\n\nQuestion 1{clickTo4}\n\n          \n          \n        \n        \n          \n          \n          \n        \n      \n    \n    \n      &amp;nbsp;\n    \n  ',
            u'from': u'default',
            u'name': u'Notification',
            u'to': u'jonasvdbrink@gmail.com',
            u'html': u'1',
            u'type': u'notification',
            u'subject': u'New submission: {form_title}'
        }],
        u'expireDate': u'No Limit',
        u'optioncolor': u'#000',
        u'sendpostdata': u'No',
        u'formWidth': u'650'
    },
    
    'questions': 
    {   
        u'1': 
        {   
            u'name': u'whatIs',
            u'allowOther': u'No',
            u'required': u'No',
            u'spreadCols': u'1',
            u'options': u'Oslo|Island|Stockholm|Paris|Keflavik|Bueno Aires',
            u'text': u'What is the capital of Norway?',
            u'qid': u'1',
            u'otherText': u'Other',
            u'type': u'control_radio',
            u'order': u'2',
            u'special': u'None',
            u'labelAlign': u'Top'
        },
        u'3': 
        {
            u'required': u'No',
            u'type': u'control_widget',
            u'name': u'clickTo3',
            u'maxWidth': u'587',
            u'settingNames': u'mjLabel,answerLabel',
            u'qid': u'3',
            u'answerLabel': u'Answer:',
            u'selectedField': u'52fb96db12597d036000002c',
            u'boxAlign': u'Left',
            u'label': u'Yes',
            u'widgetType': u'field',
            u'frameSrc': u'http://widgets.jotform.io/mathJax/',
            u'frameHeight': u'20',
            u'frameWidth': u'500',
            u'cfname': u'MathJax',
            u'order': u'3',
            u'labelAlign': u'Top'
        },
        u'2': 
        {
            u'subHeader': u'Made using quiztools',
            u'headerType': u'Large',
            u'qid': u'2',
            u'text': u'Quiz',
            u'type': u'control_head',
            u'order': u'1', 
            u'name': u'clickTo'
        }, 
        u'4': 
        {
            u'finalSrc': u'http://widgets.jotform.io/mathJax/?mjLabel=%24%24%5Cfrac%7B%5Cpartial%20%7D%7B%5Cpartial%20x%7D%20x%5E2%20%3D%202x%24%24&amp;answerLabel=%3Cempty%3E',
            u'required': u'No',
            u'type': u'control_widget',
            u'name': u'clickTo4', 
            u'maxWidth': u'587', 
            u'settingNames': 
            u'mjLabel,answerLabel',
            u'qid': u'4',
            u'answerLabel': u'',
            u'selectedField': u'52fb96db12597d036000002c',
            u'mjLabel': u'$$\\frac{\\partial }{\\partial x} x^2 = 2x$$',
            u'boxAlign': u'Left',
            u'label': u'Yes',
            u'widgetType': u'field',
            u'frameSrc': u'http://widgets.jotform.io/mathJax/',
            u'text': u'Question 1',
            u'frameHeight': u'20',
            u'frameWidth': u'500', 
            u'cfname': u'MathJax', 
            u'order': u'4', 
            u'labelAlign': u'Top'
        }
    }
}






