quiztools
=========

Tools for automating the definition of a quiz at web sites such as Kahoot, Google forms, JotForm.

More precisely, quizzes are written in DocOnce syntax in ordinary text files.
Tools in this repo can read such files and automatically create a Kahoot
quiz. Some experiments have been done with JotForm too, but so far, Kahoot
is the only site we recommend for quizzes. Kahoot has made extensions such
that mathematics and computer code can be rendered.

The key source code file is `src/KahhotQuizMaker.py`. See the test block for
how to use the software.
