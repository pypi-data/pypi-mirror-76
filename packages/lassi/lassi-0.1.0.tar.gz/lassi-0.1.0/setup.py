from setuptools import setup, find_packages

setup(
    name='lassi',
    version='0.1.0',
    packages=find_packages(where="மூலம்"),
    package_dir={"": "மூலம்"},
    url='https://lassi.readthedocs.io',
    download_url='https://github.com/julienmalard/Lassi',
    license='GNU Affero GPL 3',
    author='ਜ਼ੂਲੀਏਂ ਮਲਾਰ (Julien Malard)',
    author_email='julien.malard@mail.mcgill.ca',
    description='ਸੰਕੇਤ ਦੀ ਅਨੁਵਾਦ।',
    long_description='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=['lark-parser', 'ennikkai', 'methodtools'],
    package_data={'': ['*.lark', '*.json']}
)
