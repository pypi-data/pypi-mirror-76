from setuptools import setup
import os, io

from oneimage import __version__

here = os.path.abspath(os.path.dirname(__file__))
README = io.open(os.path.join(here, 'README.md'), encoding='UTF-8').read()
CHANGES = io.open(os.path.join(here, 'CHANGES.md'), encoding='UTF-8').read()
setup(name="oneimage",
      version=__version__,
      keywords=('oneimage', 'image', 'picture'),
      description="A simple python lib to create poster image with define data.",
      long_description=README + '\n\n\n' + CHANGES,
      long_description_content_type="text/markdown",
      url='https://github.com/sintrb/oneimage/',
      author="trb",
      author_email="sintrb@gmail.com",
      packages=['oneimage'],
      # install_requires=['pillow', 'requests'],
      zip_safe=False
      )
