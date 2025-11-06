from setuptools import setup

setup(
    name='ProjectInit',
    version='1.0.0',
    py_modules=['projectinit'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'projectinit=projectinit:main',
            'project-configs=projectinit:configure',
        ],
    },
    author='Kevo',
    description='CLI tool to create a Project repo',
    python_requires='>=3.6',
)