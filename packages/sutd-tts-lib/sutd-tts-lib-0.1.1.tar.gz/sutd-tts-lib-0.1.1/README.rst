sutd-tts-lib
======================================================

A (relatively) lightweight library for programmatically submitting entries to SUTD's Temperature Taking System, without Selenium and the like.

Submit a temperature declaration in three steps:

.. code-block:: python3

  from sutd.tts import TemperatureReading, User

  me = User("1003333", "password")
  me.login().take_temperature(TemperatureReading.OK)

Do your daily declaration while you're at it: (By default, it assumes you pressed "NO" to every checkbox)

.. code-block:: python3

  from sutd.tts import DailyDeclaration, User

  me = User("10003333", "password")
  me.login().do_daily_declaration(DailyDeclaration())

Installation
------------

.. code-block::

  pip install sutd-tts-lib

Examples
--------

Different kinds of temperature readings:

.. code-block:: python3

  from sutd.tts import TemperatureReading, User

  me = User("1003333", "password")
  me.login() # only needs to be called once
  me.take_temperature(TemperatureReading.OK)
  me.take_temperature(TemperatureReading.HIGH_TEMP_BUT_OK)
  me.take_temperature(TemperatureReading.HIGH_TEMP_NOT_OK)

****

Customize your daily declaration via the constructor or instance attributes.

This example declares that you both got served a SHN and you came into close contact with someone who also had SHN/quarantined.

.. code-block:: python3

  from sutd.tts import DailyDeclaration, User

  d = DailyDeclaration(received_SHN=True)
  d.contact_SHN = True

  me = User("1003333", "password")
  me.login().do_daily_declaration(d)


More information are available in the docstrings of the classes.

****

*Prof Chong, I don't feel so good:*

.. code-block:: python3

  from sutd.tts import DailyDeclaration, User

  d = DailyDeclaration()
  d.symptoms.dry_cough = True
  d.symptoms.fever = True

  me = User("1003333", "password")
  me.login().do_daily_declaration(d)
