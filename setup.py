from setuptools import find_packages, setup


setup(
    name='cellautoplay',
    version='0.1dev',
    description='Console-based script for playing with cellular automata.',
    author='Wyatt L Baldwin',
    author_email='self@wyattbaldwin.com',
    url='https://github.com/wylee/cellular-automata-playground',
    install_requires=['numpy'],
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    cellauto = cellautoplay.__main__:main

    """
)
