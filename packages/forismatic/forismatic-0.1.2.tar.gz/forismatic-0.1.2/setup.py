from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name="forismatic", # Replace with your own username
    description="An unofficial API wrapper for the forismatic.com API.",
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    version="0.1.2",
    author="Adam Baird",
    author_email="adamjohnbaird321@gmail.com",
    url="https://github.com/ihumanbeing/forismatic.py",
    download_url="https://pypi.org/project/forismatic.py/",
    packages=find_packages(),
    keywords=['Forismatic', 'ForismaticPy', 'Forismatic.py'],
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6'
)

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)