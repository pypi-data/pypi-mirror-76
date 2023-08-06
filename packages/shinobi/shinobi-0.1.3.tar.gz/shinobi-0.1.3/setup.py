from setuptools import setup, find_packages

# Create Short Description
DESC = '''Python `shinobi` is an Open Source Big Data Management and Analytic Service.'''

# Get Python Package Requirements
def getRequirements():
    reqs = []
    with open('requirements.txt') as fp: reqs += fp.readlines()
    reqs = map(str.strip, reqs)
    return reqs

# Initalize Package Setup Upon Pip Installation
setup(
    name = 'shinobi',
    version = '0.1.3',
    python_requires = '>=3.6',
    description = DESC,
    long_description = DESC,
    author = 'Aidan E. Dykstal',
    author_email = 'dykstala@gmail.com',
    maintainer = 'Aidan E. Dykstal',
    maintainer_email = 'dykstala@gmail.com',
    url = 'https://github.com/dykstal/shinobi',
    download_url = 'https://github.com/dykstal/shinobi/archive/v0.1.3-alpha.tar.gz',
    license = 'MIT',
    include_package_data = True,
    install_requires = getRequirements(),
    packages = find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
)
