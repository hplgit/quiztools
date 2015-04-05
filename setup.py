from distutils.core import setup

setup(name='quiztools',
      version='0.1',
      author='Jonas van den Brink, Hans Petter Langtangen',
      author_email='j.v.d.brink@fys.uio.no',
      url='https://github.com/hplgit/quiztools',
      packages=['quiztools'],
      scripts=[os.path.join('bin', 'quiztools-main.py')]
     )
