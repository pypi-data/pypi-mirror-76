# -*- coding: utf-8 -*-

"""
Guilded API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Guilded API.
:copyright: (c) 2020 NotShin
:license: MIT, see LICENSE for more details.
"""

__title__ = 'guilded'
__author__ = 'NotShin'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020 NotShin'
__version__ = '0.0.1'

class Bot:
    def __init__(self, command_prefix, **kwargs):
        self.command_prefix = command_prefix