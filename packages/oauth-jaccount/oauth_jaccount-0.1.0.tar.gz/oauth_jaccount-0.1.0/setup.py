"""
Oauth jaccount python package configuration.

tc-imba <liuyh615@sjtu.edu.cn>
"""

from setuptools import setup

setup(
    name='oauth_jaccount',
    version='0.1.0',
    author="tc-imba",
    author_email="liuyh615@126.com",
    description="python package for jaccount oauth",
    url="https://github.com/tc-imba/python-oauth-jaccount",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    packages=['oauth_jaccount'],
    include_package_data=True,
    install_requires=[
        'oauthlib',
        'PyJWT'
    ]
)
