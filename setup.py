from setuptools import setup

setup(name='twitter_lsa',
      version='0.1',
      description='A latent semantic analysis of twitter followers',
      url='https://github.com/jonstites/twitter_lsa',
      author='Jonathan Stites',
      author_email='mail@jonstites.com',
      license='MIT',
      packages=['twitter_lsa'],
      install_requires=["pylint"],
      zip_safe=False)
