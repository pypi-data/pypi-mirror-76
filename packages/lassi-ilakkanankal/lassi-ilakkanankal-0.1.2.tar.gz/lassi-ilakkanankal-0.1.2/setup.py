from setuptools import setup, find_packages

setup(
    name='lassi-ilakkanankal',
    version='0.1.2',
    packages=find_packages(where="மூலம்"),
    package_dir={"": "மூலம்"},
    url='https://github.com/lassi-samaaj/lassi-ilakkanangal',
    license='AGPL-3.0-or-later',
    author='ம. ஜூலீஎன்',
    author_email='julien.malard@mail.mcgill.ca',
    description='லஸ்ஸி மென்பொருளுக்காக இலக்கணம் விவரக்குறிப்புகள்',
    install_requires=['lark-parser'],
    package_data={'': ['*.lark', '*.json']}
)
