#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import NoOptionError


class ThresholdError(Exception):
    """Raised when the search threshold is not a float >=0.0 or <=1.0"""


class ModeError(Exception):
    """Raised when the opened file is not in mode w+"""


class SectionNameNotAllowed(Exception):
    """Raised when a section of default variant is attempted to be created."""


class MissingOptionError(NoOptionError):
    """Raised when a key cannot be found

    This could be because the key does not exist in the section or the section
    does not exist at all
    """
