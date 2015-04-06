#import quiztools.KahootQuizMaker
import sys, os, logging, pprint
sys.path.insert(0, os.pardir)
import KahootQuizMaker

def test_sample_quiz():
    """Check that kahoot quiz format is correct for .sample_quiz.quiz."""
    user = 'whoever'
    title = 'Test'
    #qm = quiztoolsKahootQuizMaker.KahootQuizMaker(
    qm = KahootQuizMaker.KahootQuizMaker(
        user, path='', loglvl=logging.DEBUG, login=False)
    filename = '.sample_quiz.quiz'
    questions = qm.read_quiz_file(filename)

    computed = qm.make_quiz(questions, title=title)
    #pprint.pprint(computed)

    expected = {
 'audience': 'University',
 'description': 'Made using quiztools.',
 'difficulty': 500,
 'language': 'English',
 'questions': [{'choices': [{'answer': 'a)', 'correct': True},
                            {'answer': 'b)', 'correct': True},
                            {'answer': 'c)', 'correct': False},
                            {'answer': 'd)', 'correct': True}],
                'iframe': {'content': u"<html><head>\n                <style>\n                    body {font-family:sans-serif;\n                          font-size:14pt;}\n                    .question {font-size:22pt;\n                               font-weight:bold;}\n                    .answer {}\n                    .letter {font-weight:bold;}\n                </style>\n                <script type='text/javascript' src='//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script></head><body><p class='question'>Which of the following cities are capitals?</p><hr><p class='answer'><span class='letter'>a)</span> Bern</p><hr><p class='answer'><span class='letter'>b)</span> Kigali</p><hr><p class='answer'><span class='letter'>c)</span> New York</p><hr><p class='answer'><span class='letter'>d)</span> Ottawa</p></body></html>"},
                'image': '',
                'numberOfAnswers': 4,
                'points': True,
                'question': '',
                'questionFormat': 2,
                'time': 60000,
                'video': {'endTime': 0,
                          'id': '',
                          'service': 'youtube',
                          'startTime': 0}},
               {'choices': [{'answer': 'a)', 'correct': False},
                            {'answer': 'b)', 'correct': False},
                            {'answer': 'c)', 'correct': False},
                            {'answer': 'd)', 'correct': True}],
                'iframe': {'content': u"<html><head>\n                <style>\n                    body {font-family:sans-serif;\n                          font-size:14pt;}\n                    .question {font-size:22pt;\n                               font-weight:bold;}\n                    .answer {}\n                    .letter {font-weight:bold;}\n                </style>\n                <script type='text/javascript' src='//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script></head><body><p class='question'>What is the capital of Norway?</p><hr><p class='answer'><span class='letter'>a)</span> Helsinki</p><hr><p class='answer'><span class='letter'>b)</span> Denmark</p><hr><p class='answer'><span class='letter'>c)</span> Drammen</p><hr><p class='answer'><span class='letter'>d)</span> Oslo</p></body></html>"},
                'image': '',
                'numberOfAnswers': 4,
                'points': True,
                'question': '',
                'questionFormat': 2,
                'time': 60000,
                'video': {'endTime': 0,
                          'id': '',
                          'service': 'youtube',
                          'startTime': 0}},
               {'choices': [{'answer': 'a)', 'correct': True},
                            {'answer': 'b)', 'correct': False},
                            {'answer': 'c)', 'correct': False}],
                'iframe': {'content': u"<html><head>\n                <style>\n                    body {font-family:sans-serif;\n                          font-size:14pt;}\n                    .question {font-size:22pt;\n                               font-weight:bold;}\n                    .answer {}\n                    .letter {font-weight:bold;}\n                </style>\n                <script type='text/javascript' src='//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script></head><body><p class='question'>This is a very famous quote:\n\n<p>\n<blockquote>\n    <em>Premature optimization is the root of all evil.</em>\n</blockquote>\n\nThis quote is attributed to</p><hr><p class='answer'><span class='letter'>a)</span> Donald Knuth</p><hr><p class='answer'><span class='letter'>b)</span> Ole-Johan Dahl</p><hr><p class='answer'><span class='letter'>c)</span> George W. Bush</p></body></html>"},
                'image': '',
                'numberOfAnswers': 3,
                'points': True,
                'question': '',
                'questionFormat': 2,
                'time': 60000,
                'video': {'endTime': 0,
                          'id': '',
                          'service': 'youtube',
                          'startTime': 0}},
               {'choices': [{'answer': 'a)', 'correct': False},
                            {'answer': 'b)', 'correct': False},
                            {'answer': 'c)', 'correct': True}],
                'iframe': {'content': u"<html><head>\n                <style>\n                    body {font-family:sans-serif;\n                          font-size:14pt;}\n                    .question {font-size:22pt;\n                               font-weight:bold;}\n                    .answer {}\n                    .letter {font-weight:bold;}\n                </style>\n                <script type='text/javascript' src='//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script></head><body><p class='question'>Compute the result of \\( a+b \\) in the case \\( a=2 \\) and \\( b=2 \\).</p><hr><p class='answer'><span class='letter'>a)</span> 5.</p><hr><p class='answer'><span class='letter'>b)</span> The computation does not make sense when \\( a \\) and \\( b \\) are given without\nunits.</p><hr><p class='answer'><span class='letter'>c)</span> 4.</p></body></html>"},
                'image': '',
                'numberOfAnswers': 3,
                'points': True,
                'question': '',
                'questionFormat': 2,
                'time': 60000,
                'video': {'endTime': 0,
                          'id': '',
                          'service': 'youtube',
                          'startTime': 0}},
               {'choices': [{'answer': 'a)', 'correct': False},
                            {'answer': 'b)', 'correct': False},
                            {'answer': 'c)', 'correct': True},
                            {'answer': 'd)', 'correct': True}],
                'iframe': {'content': u"<html><head>\n                <style>\n                    body {font-family:sans-serif;\n                          font-size:14pt;}\n                    .question {font-size:22pt;\n                               font-weight:bold;}\n                    .answer {}\n                    .letter {font-weight:bold;}\n                </style>\n                <script type='text/javascript' src='//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script></head><body><p class='question'>The equation\n\n$$\n\\begin{equation}\n\\nabla\\cdot\\boldsymbol{u} = 0\n\\label{cont:eq}\n\\end{equation}\n$$\n\nis famous in physics. Select the wrong assertion(s):</p><hr><p class='answer'><span class='letter'>a)</span> The equation tells that the vector field \\( \\boldsymbol{u} \\) is divergence free.</p><hr><p class='answer'><span class='letter'>b)</span> The equation implies that there exists a vector potential \\( \\boldsymbol{A} \\)\nsuch that \\( \\boldsymbol{u}=\\nabla\\times\\boldsymbol{A} \\).</p><hr><p class='answer'><span class='letter'>c)</span> The equation implies \\( \\nabla\\times\\boldsymbol{u}=0 \\).</p><hr><p class='answer'><span class='letter'>d)</span> The equation implies that \\( \\boldsymbol{u} \\) must be a constant vector field.</p></body></html>"},
                'image': '',
                'keywords': ['gradient',
                             'divergence',
                             'curl',
                             'vector calculus'],
                'numberOfAnswers': 4,
                'points': True,
                'question': '',
                'questionFormat': 2,
                'time': 60000,
                'video': {'endTime': 0,
                          'id': '',
                          'service': 'youtube',
                          'startTime': 0}},
               {'choices': [{'answer': 'a)', 'correct': True},
                            {'answer': 'b)', 'correct': False},
                            {'answer': 'c)', 'correct': False}],
                'iframe': {'content': u'<html><head>\n                <style>\n                    body {font-family:sans-serif;\n                          font-size:14pt;}\n                    .question {font-size:22pt;\n                               font-weight:bold;}\n                    .answer {}\n                    .letter {font-weight:bold;}\n                </style>\n                <script type=\'text/javascript\' src=\'//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML\'></script></head><body><p class=\'question\'>We want to create a Python list object of length <code>n</code> where each\nelement is <code>0</code>. Is the following code then what we need?\n\n<p>\n\n<!-- code=python (!bc pycod) typeset with pygments style "default" -->\n<div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">numpy</span>\nmylist <span style="color: #666666">=</span> numpy<span style="color: #666666">.</span>zeros(n)\n</pre></div>\n<p></p><hr><p class=\'answer\'><span class=\'letter\'>a)</span> No.</p><hr><p class=\'answer\'><span class=\'letter\'>b)</span> Yes.</p><hr><p class=\'answer\'><span class=\'letter\'>c)</span> Yes, provided we write <code>np</code> instead of <code>numpy</code>:\n\n<p>\n\n<!-- code=python (!bc pycod) typeset with pygments style "default" -->\n<div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">numpy</span> <span style="color: #008000; font-weight: bold">as</span> <span style="color: #0000FF; font-weight: bold">np</span>\nmylist <span style="color: #666666">=</span> np<span style="color: #666666">.</span>zeros(n)\n</pre></div>\n<p></p></body></html>'},
                'image': '',
                'numberOfAnswers': 3,
                'points': True,
                'question': '',
                'questionFormat': 2,
                'time': 60000,
                'video': {'endTime': 0,
                          'id': '',
                          'service': 'youtube',
                          'startTime': 0}},
               {'choices': [{'answer': 'a)', 'correct': False},
                            {'answer': 'b)', 'correct': False},
                            {'answer': 'c)', 'correct': False},
                            {'answer': 'd)', 'correct': True}],
                'iframe': {'content': u'<html><head>\n                <style>\n                    body {font-family:sans-serif;\n                          font-size:14pt;}\n                    .question {font-size:22pt;\n                               font-weight:bold;}\n                    .answer {}\n                    .letter {font-weight:bold;}\n                </style>\n                <script type=\'text/javascript\' src=\'//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML\'></script></head><body><p class=\'question\'><p>\n\n<!-- code=python (!bc pypro) typeset with pygments style "default" -->\n<div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #008000; font-weight: bold">from</span> <span style="color: #0000FF; font-weight: bold">math</span> <span style="color: #008000; font-weight: bold">import</span> sin\n\n<span style="color: #008000; font-weight: bold">def</span> <span style="color: #0000FF">D</span>(u, t, dt<span style="color: #666666">=1E-5</span>):\n    <span style="color: #008000; font-weight: bold">return</span> (u(t <span style="color: #666666">+</span> dt) <span style="color: #666666">-</span> u(t <span style="color: #666666">-</span> dt))<span style="color: #666666">/</span>(<span style="color: #666666">2*</span>dt)\n\n<span style="color: #008000; font-weight: bold">def</span> <span style="color: #0000FF">u</span>(t):\n    <span style="color: #BA2121">&quot;A quadratic function.&quot;</span>\n    <span style="color: #008000; font-weight: bold">return</span> t<span style="color: #666666">^2</span>\n\n<span style="color: #008000; font-weight: bold">print</span> D(u, t<span style="color: #666666">=4</span>),\n<span style="color: #008000; font-weight: bold">print</span> D(<span style="color: #008000; font-weight: bold">lambda</span> x: <span style="color: #008000; font-weight: bold">return</span> <span style="color: #666666">2*</span>x, <span style="color: #666666">2</span>)\n</pre></div>\n<p>\nThe purpose of this program is to differentiate the two mathematical\nfunctions\n\n$$\n\\begin{align*}\nu(t) &= t^2,\\\\\nf(x) &= 2x.\n\\end{align*}\n$$\n\nDetermine which of the following assertions that is <b>wrong</b>.</p><hr><p class=\'answer\'><span class=\'letter\'>a)</span> The <code>D</code> function computes an approximate derivative of the\nfunction <code>u(t)</code>.</p><hr><p class=\'answer\'><span class=\'letter\'>b)</span> The call <code>D(lambda x: return 2*x, 2)</code> is equivalent to defining\n\n<p>\n\n<!-- code=python (!bc pycod) typeset with pygments style "default" -->\n<div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #008000; font-weight: bold">def</span> <span style="color: #0000FF">f</span>(x):\n    <span style="color: #008000; font-weight: bold">return</span> <span style="color: #666666">2*</span>x\n</pre></div>\n<p>\nand then calling <code>D(f, 2)</code>.</p><hr><p class=\'answer\'><span class=\'letter\'>c)</span> The string in the <code>u</code> function is a valid doc string.</p><hr><p class=\'answer\'><span class=\'letter\'>d)</span> One cannot use <code>u</code> both inside the <code>D</code> function and in the\nouter calling code (the main program).</p></body></html>'},
                'image': '',
                'numberOfAnswers': 4,
                'points': True,
                'question': '',
                'questionFormat': 2,
                'time': 60000,
                'video': {'endTime': 0,
                          'id': '',
                          'service': 'youtube',
                          'startTime': 0}}],
 'quizType': 'quiz',
 'title': 'Test',
 'type': 'quiz',
 'visibility': 0}

    from deep_eq import deep_eq
    success = deep_eq(expected, computed)
    #print success
    assert success

if __name__ == '__main__':
    test_sample_quiz()
