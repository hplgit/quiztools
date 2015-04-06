# quiztools

This repo contains tools for automating the creation of a quiz at web sites such as Kahoot, Google forms, JotForm.

> The idea is to have large resources of quizzes defined in plain text in ordinar files. A specific quiz can then be quickly made by cut and paste of appropriate text. Software tools in this repo are thereafter used to *automatically create a tailored online quiz*.

## Input syntax

Quizzes are written in DocOnce syntax in ordinary text files,
see the [DocOnce Quiz Documentation](http://hplgit.github.io/doconce/doc/pub/quiz/quiz.html). A minimalistic pure text quiz with a question (`Q`),
three wrong choices (`Cw`) and one right choice (`Cr`) is specified as

```
!bquiz
Q: What is the capital of Norway?
Cw: Helsinki
Cw: Drammen
Cr: Oslo
Cw: Denmark
!equiz
```
A feature of DocOnce quizzes is the strong support for mathematics and
computer code in questions and choices. One can also add explanations why
the choices are wrong or right.

Let a file with quizzes as exemplified above have name `myquiz.do.txt`.
This file must first be processed by DocOnce to
generate the corresponding Doconce *data structure* for quizzes.
Any output format in DocOnce can be used, e.g.,

```
doconce format html myquiz.do.txt
```
Regardless of the chosen output formt,
a file with the data structure as a Python list of dictionaries
is always made: `.myquiz.quiz`. It typically looks like

```python
[{'choices': [[u'wrong', u'Helsinki']
              [u'wrong', u'Drammen']
              [u'right', u'Oslo'],
              [u'wrong', u'Denmark']],
  'no': 1,
  'question': u'What is the capital of Norway?'},
]
```

With quiztools, one can read `.quiz` files with such list of
dictionaries objects and automatically create a
[Kahoot](https://getkahoot.com) online game.

## Running quiztools

Suppose you have username `whoever` on the Kahoot web site and that
the list of dictionaries data structure (as shown above) resides in
a file `.myquiz.quiz` in the current directory.
The typical Python code to make a Kahoot quiz is then

```python
import quiztools.KahootQuizMaker
qm = quiztools.KahootQuizMaker.KahootQuizMaker('whoever')
questions = qm.read_quiz_file('.myquiz.quiz')
quiz = qm.make_quiz(questions, title='My First Quiz')
kahoot_id, url = qm.upload_quiz(quiz)
print "Uploaded quiz can be viewed at %s" % url
```

Instead of this code, one can run a program

```
quiztools-main.py whoever "My First Quiz" .myquiz.quiz
```

Go to the URL that is printed to see the online quiz!

**Note**:

 * The input to quiztools is a `.quiz` file (with a
   data structure holding the quizzes) and *not* a text file in
   DocOnce format. You must run `doconce format` on the latter
   to produce the `.quiz` file (or you can make `.quiz` files
   manually once you the [syntax](http://hplgit.github.io/doconce/doc/pub/quiz/._quiz004.html#___sec12)).


## Supported web sites for quizzes

Some experiments have been done with JotForm too, but so far, Kahoot
is the only site we strongly recommend. Kahoot has made sufficient
extensions such that mathematics and computer code can be rendered
satisfactorily.

## Installation of quiztools

Clone or fork this repository, go to `quiztools`, and run `setup.py`
the standard way

```
git clone https://github.com/hplgit/quiztools.git
cd quiztools
sudo python setup.py install
```

## Installation of DocOnce

"DocOnce": "https://github.com/hplgit/doconce" has functionality for
translating compact quiz definitions in ascii files, as outlined
above, to Kahoot data structures that can be uploaded by quiztools.
DocOnce is a quite comprehensive piece of software that depends on a
large number of packages and hence a substantial software
infrastructure. However, to use quiztools you only need a plain
DocOnce installation without the software's many dependencies.
Everything you need is installed by this command:

```
sudo pip install -e git+https://github.com/hplgit/doconce#egg=doconce --upgrade
```
You need the `pip` program and a Python version 2.7 installation.

## Status

The quiztools project is still in testing phase.  Massive online
Kahoot quiz competitions with big audiences have not been run yet.

## Authors

The quiztools software was written and tested by

 * [Jonas van den Brink](mailto:j.v.d.brink@fys.uio.no)

under the supervision of

 * [Hans Petter Langtangen](http://hplgit.github.io/homepage/index.html)
