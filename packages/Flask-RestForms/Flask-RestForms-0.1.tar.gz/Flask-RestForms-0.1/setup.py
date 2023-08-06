from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Flask-RestForms',
    packages=['flask_restforms'],
    version='0.1',
    license='MIT',
    description='Add REST superpowers to your Jinja templates',
    author='Alan Munguia Cerda',
    url='https://www.github.com/alanmunguiacerda/flask-restforms/',
    keywords=['FLASK', 'JINJA', 'REST', 'MPA'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    python_requires=">= 3.6",
    install_requires=[
        'Flask',
        'Jinja2>=2.5'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)