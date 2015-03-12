# quiztools

This repo contains tools for automating the creation of a quiz at web sites such as Kahoot, Google forms, JotForm.

> The idea is to have large resources of quizzes defined in plain text in ordinar files. A specific quiz can then be quickly made by cut and paste of appropriate text. Software tools in this repo are thereafter used to *automatically create a tailored online quiz*.

## Input syntax and supported online quiz sites

Quizzes are written in DocOnce syntax in ordinary text files,
see the [DocOnce Quiz Documentation](http://hplgit.github.io/doconce/doc/pub/quiz/quiz.html).
Tools in this repo can read such DocOnce files and automatically create a [Kahoot](https://getkahoot.com)
quiz. Some experiments have been done with JotForm too, but so far, Kahoot
is the only site we strongly recommend. Kahoot has made sufficient extensions such
that mathematics and computer code can be rendered satisfactorily.

## Program

The key source code file is `src/KahhotQuizMaker.py`. See the test block for
how to use this program.

## Status

The quiztools project is still in testing phase.  Massive online
Kahoot quiz competitions with big audiences have not been run yet.

## Authors

The quiztools software was written and tested by

 * [Jonas van den Brink](mailto:j.v.d.brink@fys.uio.no)

under the supervision of

 * [Hans Petter Langtangen](http://hplgit.github.io/homepage/index.html)
