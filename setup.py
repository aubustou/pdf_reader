from setuptools import setup

setup(
    name='pdf_reader',
    version='0.1',
    packages=[''],
    url='',
    license='MIT',
    author='Aubustou',
    author_email='survivalfr@yahoo.fr',
    description='Parse PDF',
    install_requires=[
        "pdfminer.six==20201018",
    ],
    entry_point={
        "console_scripts": [
            "parse-cv = parse_cv:main"
        ]
    }
)
