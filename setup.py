from setuptools import setup

setup(name='espn_scraper',
      version='0.13',
      description='ESPN scraper for major sports',
      url='http://github.com/andr3w321/espn_scraper',
      author='Andrew Rennhack',
      author_email='andr3w321@gmail.com',
      license='MIT',
      install_requires=[
          'pytz',
          'python-dateutil'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      packages=['espn_scraper'],
      zip_safe=False)
