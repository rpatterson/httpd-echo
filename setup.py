from setuptools import setup, find_packages
import os

version = '0.1'

test_requires = ['requests']

setup(name='httpd-echo',
      version=version,
      description=(
          "A Simple Python HTTP server that echos the request in the response"
      ),
      long_description=open(
          os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
          'Topic :: Utilities',
      ],
      keywords='httpd http echo server',
      author='Ross Patterson',
      author_email='me@rpatterson.net',
      url='https://github.com/rpatterson/httpd-echo',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'six',
      ],
      tests_require=test_requires,
      extras_require=dict(test=test_requires),
      test_suite='tests',
      entry_points=dict(console_scripts=['httpd-echo=httpdecho:main']),
      )
