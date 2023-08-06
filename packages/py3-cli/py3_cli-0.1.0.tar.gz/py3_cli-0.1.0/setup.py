from setuptools import setup

setup(name='py3_cli',
      version='0.1.0',
      description='py3-cli - a simple python library for creating CLI, implemented by calling functions using commands.',
      long_description='py3-cli is a framework for creating simple and correct command-line applications in Python. This framework has a full configuration and amazing flexibility of creating commands, in addition, the framework has its own logging which can also be configured for yourself.',
      packages=['py3_cli'],
      author_email='jklenot123@gmail.com',
      zip_safe=False,
      url="https://github.com/JkLEnot/py3_cli/",
      author="JkLEnot",
      install_requires=[
            "termcolor==1.1.0",
      ])