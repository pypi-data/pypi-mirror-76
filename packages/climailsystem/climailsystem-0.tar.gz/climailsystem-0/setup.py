from setuptools import setup, find_packages
setup(
    name='climailsystem',
    version='0',
    author = 'Akshit Ahuja',
    author_email = "techsyapa@gmail.com",
    description = "A small Package for sending and reading mails from cli",
    url = "https://github.com/aksh45/climailsystem",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['sendmail'],
    include_package_data=True,
    install_requires=[
        'Click','pybase64','google-api-python-client','google-auth-httplib2','google-auth-oauthlib'
    ],
    entry_points='''
        [console_scripts]
        sendmail=sendmail.__main__:main
    ''',
)
