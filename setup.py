# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='wikigeolinks',
    version='0.1.3',
    description='A web service to access georeferenced articles of the Wikipedia and their relations',
    author='Adria Mercader',
    author_email='amercadero@gmail.com',
    url='http://amercader.net/dev/wikipedia',
    install_requires=[
        "Pylons>=1.0",
        "SQLAlchemy>=0.5",
        "MapFish>=2.0",
        "psycopg2",
        "egenix-mx-base"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'wikigeolinks': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'wikigeolinks': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['MapFish', 'PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = wikigeolinks.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
