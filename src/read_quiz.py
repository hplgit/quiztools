def read_quiz_file(infile):
    with open(infile) as f:
        quiz = eval(f.read())
    assert type(quiz) == list
    assert type(quiz[0]) == dict

    for q in quiz:
        q.pop('no', None)
        for i, c in enumerate(q['choices']):
            q['choices'][i] = {"answer" : c[1],
                "correct" : c[0] == u'right'}

        q["numberOfAnswers"] = i+1
        q["questionFormat"] = 1
        q["time"] = 60000
        q["image"] = ""
        q["video"] = {"id" : "",
                      "startTime" : 0,
                      "endTime" : 0,
                      "service" : "youtube"}
        q["points"] = True

    return quiz

questions = read_quiz_file("../demo-quiz/.test_jonas.quiz")

quiz_dict = {'title' : 'Quiztools test quiz!',
             'questions' : questions,
             'quizType': 'quiz',
             'visibility': 0,  # 0: private, 1: public
             'type': 'quiz',
             'difficulty': 500,
             'audience': 'University',
             'language': 'English',
             'description': 'Test quiz of quiztools'
}
