from setuptools import setup

setup(name='comment_generator',
      version='0.1',
      description='Learn to comment',
      url='https://github.com/jonstites/comment_generator',
      author='Jonathan Stites',
      author_email='mail@jonstites.com',
      license='MIT',
      packages=['comment_generator'],
      install_requires=[
          "argh"
          ],
      zip_safe=False)
