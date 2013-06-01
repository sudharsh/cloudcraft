#!/usr/bin/env python

from distutils.core import setup

setup(name="Cloudcraft",
      license="BSD",
      version="0.1",
      description="Easy minecraft and bukkit server management",
      author="Sudharshan S",
      author_email="sudharsh@gmail.com",
      url="https://github.com/sudharsh/cloudcraft",
      packages=['cloudcraft'],
      package_data={'cloudcraft': ['scripts/*.sh', 'config/*.template']},
      scripts=['bin/cloudcraft']
      )
      


      
      
