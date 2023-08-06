import os
import setuptools

setuptools.setup(
    name=''+os.getenv('PackageName')+'',
    version=''+os.getenv('MajorVersion')+'.'+os.getenv('MinorVersion')+'.'+os.getenv('Patches')+'.'+os.getenv('pushcounter')+'',
    packages=['Studio2V'],
    url='',
    license='',
    setup_requires=['wheel'],
    author='chinnamgaric',
    author_email='',
    description='',
)

