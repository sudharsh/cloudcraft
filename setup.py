#!/usr/bin/env python

from distutils.core import setup

setup(name="Cloudcraft",
      license="BSD",
      version="0.1.4",
      description="Easy minecraft and bukkit server management",
      long_description="Cloudcraft is a toolbelt to manage bukkit servers easily on the cloud",
      author="Sudharshan S",
      author_email="sudharsh@gmail.com",
      url="https://github.com/sudharsh/cloudcraft",
      packages=['cloudcraft'],
      package_data={'cloudcraft': ['scripts/*.sh', 'config/*.template']},
      scripts=['bin/cloudcraft'],

      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: Utilities'
        ],

      install_requires=["Fabric==1.6.1",
                        "boto==2.9.4",
                        "paramiko==1.10.1"],
      requires=["Fabric (==1.6.1)",
                "boto (==2.9.4)",
                "paramiko (==1.10.1)"]
      )
      


      
      
