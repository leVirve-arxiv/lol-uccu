from setuptools import setup

setup(name='LOL-UCCU',
      version='1.0',
      description='OpenShift App',
      author='Salas',
      author_email='salas@salas.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.10.1',
			'Flask-PyMongo>=0.3.0',
			'pymongo>=2.7.2',
			'requests>=2.5.0'
			],
     )
