==================================================================
confer: A configuration preparation library for python project
==================================================================

External configuration::

  # settings.py
  COLOR = 'blue'
  NUMBER = 6

  # settings_extra.py
  COLOR = 'yellow'
  NAME = 'Arthur'

Configuration body example (config.py)::

  from confer import configure

  configure(
      'file:///path/to/settings.py',
      'file:///path/to/settings_extra.py',
      ...
  )

Yields::

  >>> import config
  >>> config.COLOR
  'yellow'
  >> config.NUMBER
  6
  >> config.NAME
  'Arthur'
  
