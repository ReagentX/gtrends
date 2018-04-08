from setuptools import setup, find_packages

setup(
    name='gtrends',
    version='1.0',
    description='A Python 3 scraper designed to tabulate data from HLTV.org',
    author='Christopher Sardegna',
    author_email='github@reagentx.net',
    install_requires=['pytrends'],
    packages=find_packages(),
    scripts=['scripts/run.py']
)
