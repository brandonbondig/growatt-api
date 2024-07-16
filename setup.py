from setuptools import setup, find_packages

setup(
    name='growatt',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    # entry_points={
    #     'console_scripts': [
    #         'growatt=growatt.growatt:main',  # Assuming you have a main function in growatt.py
    #     ],
    # },
    author='Brandon Bondig',
    author_email='brandon@bondig.dk',
    description='A Python wrapper for Growatt API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/brandonbondig/growatt',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)