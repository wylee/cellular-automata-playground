from distutils.core import setup


setup(
    name='cellautoplay',
    version='0.1dev',
    description='Console-based script for playing with cellular automata.',
    author='Wyatt L Baldwin',
    author_email='self@wyattbaldwin.com',
    url='https://bitbucket.org/wyatt/cellular-automata-playground',
    install_requires=('numpy',),
    packages=('cellautoplay',),
    entry_points="""
    [console_scripts]
    cellauto = cellautoplay.__main__:main
    """
)
