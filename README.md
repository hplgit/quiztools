# quiztools

This repo contains tools for automating the creation of a quiz at web sites such as Kahoot, Google forms, JotForm.

> The idea is to have large resources of quizzes defined in plain text in ordinar files. A specific quiz can then be quickly made by cut and paste of appropriate text. Software tools in this repo are thereafter used to *automatically create a tailored online quiz*.

## Input syntax and supported online quiz sites

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

With quiztools, one can read DocOnce files with quizzes
and automatically create a [Kahoot](https://getkahoot.com)
online game.

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
