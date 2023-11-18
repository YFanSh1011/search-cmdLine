from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='search_cmdline',
    version='1.0.0',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'search=search_cmdline.main:main'
        ]
    },
    include_package_data=True,
    package_data={
        'search_cmdline': ['configs/*.json'],
    },
    author='Yuefan Shang',
    author_email='yfanshang1011@gmail.com',
    description='A customisable command line tool that allows user to perform search using different browsers and search engines... And more',
)
