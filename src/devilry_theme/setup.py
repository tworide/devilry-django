from setuptools import setup, find_packages


setup(name = 'devilry_theme',
      description = 'The devilry theme (ExtJS theme + custom CSS).',
      version = '1.0',
      license='BSD',
      author = 'Espen Angell Kristiansen',
      packages=find_packages(exclude=['ez_setup']),
      install_requires = ['setuptools'],
      include_package_data=True,
      long_description = open('README.rst').read(),
      zip_safe=False,
      classifiers=[
                   'Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Operating System :: OS Independent'
                  ]
)
