# quiztools

Tools for automating the definition of a quiz at web sites such as Kahoot, Google forms, JotForm.
The idea is to have large resources of quizzes defined in plain text in ordinar files. A specific quiz can then be quickly made by cut and paste of appropriate text. Software tools in this repo are thereafter used to automatically create a tailored online quiz.

More precisely, quizzes are written in DocOnce syntax in ordinary text files.
Tools in this repo can read such files and automatically create a Kahoot
quiz. Some experiments have been done with JotForm too, but so far, Kahoot
is the only site we recommend for quizzes. Kahoot has made extensions such
that mathematics and computer code can be rendered.

The key source code file is `src/KahhotQuizMaker.py`. See the test block for
how to use the software.
