try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
import os

cwd = os.getcwd()
sys.path.append(os.path.join(
    cwd, 'vmreact/pre-requirements/vmreact_miniconda2/envs/vmreact_conda/bin'))
print sys.path
required = [
    'certifi==2018.8.13',
    'numpy==1.14.3',
    'pandas==0.23.4',
    'python-dateutil==2.7.3',
    'pytz==2018.5',
    'six==1.11.0',
    'virtualenv==16.0.0'

]

long_desc = open('README.md').read() + '\n\n' + \
    open('requirements.txt').read() + '\n\n' + open('installation.txt').read()

setup(
    name='vmreact',
    version='0.1',
    packages=[
        'vmreact-master.scripts', 'vmreact-master.scripts.grader', 'vmreact-data-visualization',
        'vmreact-mturk.mturk_api_launch_scripts', 'vmreact-mturk.stats', 'vmreact-mturk.post_scoring_compiled_csv'
    ],
    install_requires=required,
    platforms='Mac OSx',
    url='https://github.com/daelsaid/vmreact',
    license='',
    author='dawlat el-said',
    author_email='daelsaid@gmail.com',
    description='Etkin lab VMREACT package',
    long_description=long_desc
)
