from setuptools import setup, find_packages

setup(
    name='hltv-scraper',
    version='1.0',
    description='A Python 3 scraper designed to tabulate data from HLTV.org',
    author='Christopher Sardegna',
    author_email='github@reagentx.net',
    install_requires=['requests', 'requests-cache'],
    packages=find_packages(),
    scripts=['scripts/scrape-hltv.py', 'scripts/upcoming.py']
)
