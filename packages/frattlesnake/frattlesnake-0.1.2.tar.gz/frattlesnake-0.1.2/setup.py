# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frattlesnake']

package_data = \
{'': ['*']}

install_requires = \
['pyjnius>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'frattlesnake',
    'version': '0.1.2',
    'description': "frattlesnake is a bridge and library from KoLmafia's Java environment to a Python environment",
    'long_description': 'frattlesnake\n===\n\n<img class="snake" src="https://cdn.coldfront.net/thekolwiki/images/a/a6/Snakeboss2.gif" style="height:1.5em" />\n\n`frattlesnake` is a bridge and library from KoLmafia\'s Java environment to a Python environment. It is extremely 🚧 under construction 🚧 but it is usable!\n\nFor now just clone this repo and play with the examples. It will even download the latest `kolmafia.jar` for you to hook into.\n\nRequirements\n====\n\n* Python 3.8+\n* I am running the same version of Java that was used to compile the JAR on the build server just in case.\n\nDevelopment\n===\n\n```shell\npoetry install\n```\n\nto install our dependencies and then just run your file! You may need to manually specify the path to your `libjvm.so`. For example, on my machine I needed to run\n\n```shell\nJVM_PATH=~/.jenv/versions/1.8/jre/lib/amd64/server/libjvm.so python ./example.py\n```\n\nbecause I use `jEnv` to manage my Java versions. And that path is totally different in my Java 11 directory so it\'s a pain for now.\n',
    'author': 'Samuel Gaus',
    'author_email': 'sam@gaus.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gausie/frattlesnake',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
