try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
        'description': 'Space Invaders Pygame clone',
        'author': 'Jonathan Yeong',
        'version': '0.1.0',
        'install_requires': ['nose'],
        'packages': ['pyvader'],
        'scripts': [],
        'name': 'PyVader'
}

setup(**config)
