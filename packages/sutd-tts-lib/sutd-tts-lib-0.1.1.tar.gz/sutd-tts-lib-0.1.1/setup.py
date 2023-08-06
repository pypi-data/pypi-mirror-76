# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sutd', 'sutd.tts']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'fake-headers>=1.0.2,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'sutd-tts-lib',
    'version': '0.1.1',
    'description': "A (relatively) lightweight library for programmatically submitting entries to SUTD's Temperature Taking System, without Selenium and the like.",
    'long_description': 'sutd-tts-lib\n======================================================\n\nA (relatively) lightweight library for programmatically submitting entries to SUTD\'s Temperature Taking System, without Selenium and the like.\n\nSubmit a temperature declaration in three steps:\n\n.. code-block:: python3\n\n  from sutd.tts import TemperatureReading, User\n\n  me = User("1003333", "password")\n  me.login().take_temperature(TemperatureReading.OK)\n\nDo your daily declaration while you\'re at it: (By default, it assumes you pressed "NO" to every checkbox)\n\n.. code-block:: python3\n\n  from sutd.tts import DailyDeclaration, User\n\n  me = User("10003333", "password")\n  me.login().do_daily_declaration(DailyDeclaration())\n\nInstallation\n------------\n\n.. code-block::\n\n  pip install sutd-tts-lib\n\nExamples\n--------\n\nDifferent kinds of temperature readings:\n\n.. code-block:: python3\n\n  from sutd.tts import TemperatureReading, User\n\n  me = User("1003333", "password")\n  me.login() # only needs to be called once\n  me.take_temperature(TemperatureReading.OK)\n  me.take_temperature(TemperatureReading.HIGH_TEMP_BUT_OK)\n  me.take_temperature(TemperatureReading.HIGH_TEMP_NOT_OK)\n\n****\n\nCustomize your daily declaration via the constructor or instance attributes.\n\nThis example declares that you both got served a SHN and you came into close contact with someone who also had SHN/quarantined.\n\n.. code-block:: python3\n\n  from sutd.tts import DailyDeclaration, User\n\n  d = DailyDeclaration(received_SHN=True)\n  d.contact_SHN = True\n\n  me = User("1003333", "password")\n  me.login().do_daily_declaration(d)\n\n\nMore information are available in the docstrings of the classes.\n\n****\n\n*Prof Chong, I don\'t feel so good:*\n\n.. code-block:: python3\n\n  from sutd.tts import DailyDeclaration, User\n\n  d = DailyDeclaration()\n  d.symptoms.dry_cough = True\n  d.symptoms.fever = True\n\n  me = User("1003333", "password")\n  me.login().do_daily_declaration(d)\n',
    'author': 'Chester',
    'author_email': 'chester8991@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chesnutcase/sutd-tts-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
