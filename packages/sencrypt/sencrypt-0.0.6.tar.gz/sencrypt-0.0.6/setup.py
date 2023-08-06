from setuptools import setup

setup(
    name = 'sencrypt',
    version = '0.0.6',
    author='Vipin Kasarla',
    author_email='vipink70@gmail.com',
    description= 'tool to test and encrypt s3 buckets',
    license = 'GPLv3+',
    url='',
    packages=['sencrypt'],
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        sencrypt=sencrypt.sencrypt:cli
    '''

)