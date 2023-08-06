#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import ast
import json
import shutil
from difflib import SequenceMatcher
from pyconfigreader.exceptions import (ModeError, SectionNameNotAllowed,
                                       ThresholdError, MissingOptionError)
from collections import OrderedDict
from copy import deepcopy

from configparser import (ConfigParser, NoSectionError,
                          NoOptionError, DuplicateSectionError)

from io import StringIO

CASE_SENSITIVE = False
ALLOW_NO_VALUE = True
DEFAULT_DICT = OrderedDict([('reader', 'configreader')])


def load_defaults(filename, case_sensitive=CASE_SENSITIVE):
    """Returns a dictionary of the configuration properties

    :param filename: the name of an existing ini file
    :param case_sensitive: determines whether keys should retain their
        alphabetic cases or be converted to lowercase
    :type filename: str
    :type case_sensitive: bool
    :returns: sections, keys and options read from the file
    :rtype: OrderedDict
    """
    configs = OrderedDict()
    parser = ConfigParser(allow_no_value=ALLOW_NO_VALUE)
    if case_sensitive:
        parser.optionxform = str
    parser.read(filename)

    for section in parser.sections():
        configs[section] = OrderedDict(parser.items(section))
    return configs


class ConfigReader(object):
    """A simple configuration reader class for performing
    basic config file operations including reading, setting
    and searching for values.

    It is preferred that the value of ``filename`` be an absolute path.
    If ``filename`` is not an absolute path, then the configuration (ini) file
    will be saved at the Current Working directory (the value of :func:`~os.getcwd`).

    If ``file_object`` is an open file then ``filename`` shall point to it's path

    :usage:

    >>> from pyconfigreader import ConfigReader
    >>> config = ConfigReader(filename='config.ini')
    >>> config.set('version', '2')  # Saved to section `main`
    >>> config.set('Key', 'Value', section='Section')   # Creates a section `Section` on-the-fly
    >>> config.set('name', 'main')
    >>> name = config.get('name')
    >>> default_section = config.get_items('main')
    >>> config.close(save=True)  # Save on close
    >>> # Or explicitly call
    >>> # config.save()
    >>> # config.close()

    :param str filename: The name of the final config file. Defaults to `settings.ini`.
    :param file_object: A file-like object opened in mode w+.
        Defaults to a new StringIO object.
    :param bool case_sensitive: Determines whether keys should retain their
        alphabetic cases or be converted to lowercase. Defaults to `True`.
    :type file_object: Union[_io.TextIOWrapper, TextIO, io.StringIO]

    :ivar str filename: Path to the ini file
    :ivar OrderedDict sections: The sections in the ini file
    """

    __defaults = deepcopy(DEFAULT_DICT)
    __default_section = 'main'

    def __init__(self, filename='settings.ini', file_object=None,
                 case_sensitive=CASE_SENSITIVE):
        self.__parser = ConfigParser(allow_no_value=ALLOW_NO_VALUE)
        self.case_sensitive = case_sensitive
        if case_sensitive:
            self.__parser.optionxform = str
        self.__filename = self._set_filename(filename)
        self.__file_object = self._check_file_object(file_object)
        self._create_config()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def sections(self):
        return self._get_sections()

    @sections.setter
    def sections(self, value):
        raise AttributeError("'Can't set attribute")

    @property
    def filename(self):
        return self._get_filename()

    @filename.setter
    def filename(self, value):
        self.__filename = self._set_filename(value)
        try:
            self.__file_object.mode
            self.__file_object = self._get_new_object()
            self.__filename = self.__file_object.name
        except AttributeError:
            pass

    def _get_sections(self):
        return self.__parser.sections()

    def _get_filename(self):
        return self.__filename

    def _get_new_object(self):
        """Copies the contents of the old file into a buffer
        and deletes the old file.

        To write to disk call :func:`~pyconfigreader.reader.ConfigReader.save`
        """
        new_io = StringIO()
        new_io.truncate(0)

        self.__file_object.seek(0)

        content = self.__file_object.read()
        new_io.write(content)

        self.__file_object.close()
        os.remove(self.__file_object.name)
        return new_io

    def _check_file_object(self, file_object):
        """Check if file_object is readable and writable

        If file_object if an open file, then :attr:`reader.ConfigReader.filename`
        is set to point at the path of file_object.

        :param file_object: Union[StringIO, TextIO]
        :raises ModeError: If file_object is not readable and writable
        :return: Returns the file object
        :rtype: Union[StringIO, TextIO]
        """
        if file_object is None:
            file_object = StringIO()
        if not isinstance(file_object, StringIO):
            if file_object.mode != 'w+':
                raise ModeError("Open file not in mode 'w+'")

            self.__filename = os.path.abspath(file_object.name)

        return file_object

    @staticmethod
    def _set_filename(value):
        """Set the file name provided to a full path

        If the filename provided is not an absolute path
        the ini file is stored at the current working directory -
        the value of ``os.getcwd()``.

        :param value: The new file name or path
        :type value: str
        :returns: the full path of the file
        :rtype: str
        """
        if os.path.isabs(value):
            if not os.path.isdir(os.path.dirname(value)):
                raise FileNotFoundError('Directory does not exist')
            full_path = value
        else:
            full_path = os.path.join(os.path.abspath(
                os.getcwd()), os.path.basename(value))
        return full_path

    def _add_section(self, section):
        """Add a section to the ini file if it doesn't exist

        :param section: The name of the section
        :type section: str
        :returns: Nothing
        :rtype: None
        """
        if section.lower() == 'default':
            raise SectionNameNotAllowed("Section name '{}' cannot be created. See "
                                        "<https://stackoverflow.com/questions/124692/what-is-the-intended-use-of-the"
                                        "-default-section-in-config-files-used-by-configpa>".format(section))

        try:
            self.__parser.add_section(section)
        except DuplicateSectionError:
            pass

    def _write_config(self):
        """Write to the file-like object

        :returns: Nothing
        :rtype: None
        """
        self.__file_object.seek(0)
        self.__parser.write(self.__file_object)

    def reload(self):
        """Reload the configuration file into memory"""
        self.__defaults = deepcopy(DEFAULT_DICT)
        for i in self.sections:
            self.remove_section(i)
        self._create_config()

    def _create_config(self):
        """Initialise an ini file from the defaults provided

        This does not write the file to disk. It only reads
        from disk if a file with the same name exists.

        :returns: Nothing
        :rtype: None
        """
        defaults = load_defaults(self.filename, self.case_sensitive)
        data = deepcopy(self.__defaults)
        data.update(defaults)

        for key, value in data.items():
            if isinstance(value, OrderedDict):
                self._add_section(key)
                self._set_many(value, section=key)

            else:
                section = self.__default_section
                self._add_section(section)
                self._set(key, value, section)

        self._write_config()

    @staticmethod
    def _evaluate(value):
        value_ = str(value)
        try:
            result = ast.literal_eval(value_)
        except (ValueError, SyntaxError):
            # ValueError when normal string
            # SyntaxError when empty
            result = os.path.expandvars(str(value_))

        return result

    @staticmethod
    def _separate_prefix(key, prefix):
        try:
            r_key = key.rsplit(prefix + '_', 1)
        except ValueError:
            final_key = key
        else:
            final_key = ''.join(r_key)

        return final_key

    def get(self, key, section=None, evaluate=True,
            default=None, default_commit=False):
        """Return the value of the provided key

        Returns None if the key does not exist.
        The section defaults to **main** if not provided.
        If the value of ``key`` does not exist and ``default`` is not None,
        the value of ``default`` is returned. And if ``default_commit`` is True, then
        the value of ``default`` is written to file on disk immediately.

        If ``evaluate`` is True, the returned values are evaluated to
        Python data types int, float and boolean.

        .. versionchanged:: 0.5.0

            Expands shell variables while leaving unknown ones unchanged.

        .. versionchanged:: 0.4.0

            Raises NoOptionError when a non-existent key is fetched.

        .. versionchanged:: 0.7.0

            Replaced NoOptionError with :exc:`~pyconfigreader.exceptions.MissingOptionError` for py2.7 compatibility.

        :param key: The key name
        :param section: The name of the section, defaults to **main**
        :param evaluate: Determines whether to evaluate the acquired values into Python literals
        :param default: The value to return if the key is not found
        :param default_commit: Also write the value of default to ini file on disk
        :type key: str
        :type section: str
        :type evaluate: bool
        :type default: str
        :type default_commit: bool
        :raises MissingOptionError: When the key whose value is being fetched does not exist in the section
        :returns: The value that is mapped to the key or None if not found
        :rtype: Union[str, int, float, bool, None]
        """
        section = section or self.__default_section
        try:
            value = self.__parser.get(section, option=key)

        except (NoSectionError, NoOptionError):
            if default is None:
                raise MissingOptionError(key, section)

            value = default
            self.set(key, value, section, commit=default_commit)

        if evaluate:
            value = self._evaluate(value)

        return value

    def set(self, key, value, section=None, commit=False):
        """Sets the value of key to the provided value

        Section defaults to **main** if not provided.
        The section is created if it does not exist.

        When ``commit`` is True, all changes up to the current
        one are written to disk.

        :param key: The key name
        :param value: The value to which the key is mapped
        :param section: The name of the section, defaults to **main**
        :param commit: Also write changes to ini file on disk
        :type key: str
        :type value: str
        :type section: str
        :type commit: bool
        :rtype: None
        """
        _section = self._get_valid_section(section)
        self._set(key, value, _section)
        self._propagate_changes(commit)

    def _propagate_changes(self, commit):
        self._write_config()
        if commit:
            self.save()

    def _get_valid_section(self, section):
        _section = section or self.__default_section
        self._add_section(_section)
        return _section

    def _set(self, key, value, section=None):
        try:
            self.__parser.set(section, option=key, value=str(value))
        except ValueError:
            # String interpolation error
            value = value.replace('%', '%%').replace('%%(', '%(')
            self.__parser.set(section, option=key, value=value)

    def _set_many(self, data, section):
        for _key, _value in data.items():
            self._set(key=_key, value=_value, section=section)

    def set_many(self, data, section=None, commit=False):
        """Update multiple keys

        This is a convenience method that is much faster to utilise than using
        :func:`~pyconfigreader.reader.ConfigReader.set` for every key.

        .. versionadded:: 0.6.0

        :param dict data: Data to update in the configuration file
        :param str section: The section to update with the data
        :param bool commit: If True, write, instantly, all change to file. Defaults to False.
        """
        _section = self._get_valid_section(section)
        self._set_many(data, _section)
        self._propagate_changes(commit)

    def get_items(self, section):
        """Returns an OrderedDict of items (keys and their values) from a section

        The values are evaluated into Python literals, if possible.

        Returns None if section is not found.

        :param section: The section from which items (key-value pairs) are to be read from
        :type section: str
        :return: An dictionary of keys and their values
        :rtype: Union[OrderedDict, None]
        """

        if section not in self.sections:
            return None

        d = OrderedDict()
        for key, v in self.__parser.items(section):
            value = self._evaluate(v)
            d[key] = value
        return d

    def remove_section(self, section):
        """Remove a section from the configuration file
        whilst leaving the others intact

        :param section: The name of the section to remove
        :type section: str
        :returns: Nothing
        :rtype: None
        """
        self.__file_object.seek(0)  # to avoid configparser.MissingSectionHeaderError
        self.__parser.read_file(self.__file_object, source=self.filename)
        self.__parser.remove_section(section)
        self._write_config()
        self.__file_object.truncate()

    def remove_option(self, key, section=None, commit=False):
        """Remove an option from the configuration file

        :param key: The key name
        :param section: The section name, defaults to **main**
        :param commit: Also write changes to ini file on disk
        :type key: str
        :type section: str
        :type commit: bool
        :returns: Nothing
        :rtype: None
        """
        section = section or self.__default_section
        self.__file_object.seek(0)  # to avoid configparser.MissingSectionHeaderError
        self.__parser.read_file(self.__file_object, source=self.filename)
        self.__parser.remove_option(section=section, option=key)
        self._write_config()
        self.__file_object.truncate()
        if commit:
            self.save()

    def remove_key(self, *args, **kwargs):
        """Same as calling :func:`~pyconfigreader.reader.ConfigReader.remove_option`

        This is just in case one is used to the key-value term pair
        """
        self.remove_option(*args, **kwargs)

    def show(self, output=True):
        """Prints out all the sections and
        returns a dictionary of the same

        :param output: Print to std.out a string representation of the file contents, defaults to True
        :type output: bool
        :returns: A dictionary mapping of sections, options and values
        :rtype: dict
        """
        configs = OrderedDict()
        string = '{:-^50}'.format(
            os.path.basename(self.filename))

        for section in self.sections:
            configs[section] = OrderedDict()
            options = self.__parser.options(section)
            string += '\n{:^50}'.format(section)

            for option in options:
                value = self.get(option, section)
                configs[section][str(option)] = value
                string += '\n{:>23}: {}'.format(option, value)

            string += '\n'

        string += '\n\n{:-^50}\n'.format('end')
        if output:
            print('\n\n{}'.format(string))
        return configs

    def search(self, value, case_sensitive=True,
               exact_match=False, threshold=0.36):
        """Returns a tuple containing the key, value and
        section of the best match found, else empty tuple

        If ``exact_match`` is False, checks if there exists a value that matches
        above the threshold value. In this case, ``case_sensitive`` is ignored.

        If ``exact_match`` is True then the value of ``case_sensitive`` matters.

        The ``threshold`` value should be 0, 1 or any value
        between 0 and 1. The higher the value the better the accuracy.

        .. versionchanged:: 0.5.0

            Returns all the matches found

        :param value: The value to search for in the config file
        :param case_sensitive: Match case during search or not
        :param exact_match: Match exact value
        :param threshold: The value of matching at which a match can be considered as satisfactory
        :type value: str
        :type case_sensitive: bool
        :type exact_match: bool
        :type threshold: float
        :returns: A tuple of the key, value and section of the results, else None
        :rtype: Union[tuple, None]
        """
        if not 0 <= threshold <= 1:
            raise ThresholdError(
                'threshold must be a float in the range of 0 to 1')
        lowered_value = value.lower()
        matches = []
        for section in self.sections:
            options = self.__parser.options(section)

            for key in options:
                found = self.get(key, section, evaluate=False)
                if exact_match:
                    if case_sensitive:
                        if value == found:
                            result = (key, found, section)
                            return result
                    else:
                        if lowered_value == found.lower():
                            result = (key, found, section)
                            return result
                else:
                    ratio = SequenceMatcher(None, found, value).ratio()
                    if ratio >= threshold:
                        result = (ratio, key, found, section)
                        matches.append(result)
        if matches:
            best_match = sorted(matches, reverse=True)
            return tuple(i[1:] for i in best_match)
        else:
            return None

    def to_json(self, file_object=None):
        """Export config to JSON

        If a ``file_object`` is given, it is exported to it
        else returned as called

        :usage:

        >>> # Example
        >>> reader = ConfigReader()
        >>> with open('config.json', 'w') as f:
        ...     reader.to_json(f)
        >>> # or
        >>> from io import StringIO
        >>> s_io = StringIO()
        >>> reader.to_json(s_io)
        >>> reader.close()

        :param file_object: A file-like object for the JSON content
        :type file_object: io.TextIO
        :returns: A string or the dumped JSON contents or nothing if file_object is provided
        :rtype: str or None
        """
        config = self.show(output=False)
        if file_object is None:
            return json.dumps(config, indent=4)
        else:
            try:
                json.dump(config, file_object, indent=4)
            except TypeError:
                string = json.dumps(config, indent=4)
                file_object.write(string.decode('utf-8'))

    def load_json(self, filename='settings.json', section=None,
                  identifier='@', encoding=None):
        """Load config from JSON file

        For instance::

            # With ``identifier`` as '@',
            '@counters': {
                'start': {
                    'name': 'scrollers',
                    'count': 15
                },
                'end': {
                    'name': 'keepers',
                    'count': 5
                }
            }

            # will result in a section
            [counters]
            start = {'name': 'scrollers', 'count': 15}
            end = {'name': 'keepers', 'count': 5}

        :param filename: name of the JSON file
        :param section: config section name to save key and values by default
        :param identifier: the prefix that identifies a key as a section name
        :param encoding: encoding of the JSON file
        :type filename: str
        :type section: str
        :type identifier: str
        :type encoding: str
        :return: nothing
        """
        with open(filename, 'r', encoding=encoding) as f:
            contents = f.read()

        data = json.loads(contents)

        for key in data.keys():
            value = data[key]
            if key.startswith(identifier):
                key = key[1:]
                self._add_section(key)

                for item in value.keys():
                    self.set(key=item,
                             value=value[item],
                             section=key)
            else:
                _section = section or self.__default_section
                self._add_section(_section)
                self.set(key, value, _section)

    def to_env(self, environment=None, prepend=True):
        """Export contents to an environment

        Exports by default to :data:`os.environ`.

        By default, the section and option would be capitalised
        and joined by an underscore to form the key - as an
        attempt at avoid collision with (any) environment variables.

        :usage:

        >>> reader = ConfigReader()
        >>> reader.show(output=False)
        OrderedDict([('main', OrderedDict([('reader', 'configreader')]))])
        >>> reader.to_env()
        >>> import os
        >>> os.environ['MAIN_READER']
        'configreader'
        >>> reader.to_env(prepend=False)
        >>> os.environ['READER']
        'configreader'
        >>> reader.close()

        :param environment: An environment to export to
        :param prepend: Prepend the section name to the key
        :type environment: :data:`os.environ`
        :type prepend: bool
        :returns: Nothing
        :rtype: None
        """
        environment = environment or os.environ
        data = self.show(False)

        for section in data:
            items = data[section]

            for item in items:
                if prepend:
                    env_key = '{}_{}'.format(section, item).upper()
                else:
                    env_key = item.upper()

                environment[env_key] = str(items[item])

    def save(self):
        """Write to file on disk

        Write the contents to a file on the disk.

        This does not close the file. You have to explicitly call
        :func:`~pyconfigreader.reader.ConfigReader.close` to do so.

        :returns: Nothing
        :rtype: None
        """
        if isinstance(self.__file_object, StringIO):
            with open(self.filename, 'w') as config_file:
                self.__file_object.seek(0)
                shutil.copyfileobj(self.__file_object, config_file)
        else:
            self.__file_object.flush()
            os.fsync(self.__file_object.fileno())

    def close(self, save=False):
        """Close the file-like object

        If ``save`` is True, the contents are written to the file on disk first .

        :param save: write changes to disk
        :type save: bool
        """
        if save:
            self.save()
        self.__file_object.close()
        del self.__file_object

    def load_env(self, environment=None, prefix='', commit=False):
        """Load alphanumeric environment variables into configuration file

        Default environment is provided by :data:`os.environ`.

        The ``prefix`` is used to filter keys in the environment which
        start with the value. This is an adaptive mode to :func:`~pyconfigreader.reader.ConfigReader.to_env`
        which prepends the section to the key before loading it to the
        environment.

        :param environment: the environment to load from
        :param prefix: only keys which are prefixed with this string are loaded
        :param commit: write to disk immediately
        :type environment: os._Environ
        :type prefix: str
        :type commit: bool
        :return: nothing
        """
        env = environment or os.environ
        prefix = prefix.strip()
        pref = prefix.upper()

        if pref:
            items = {self._separate_prefix(k, pref): v
                     for k, v in env.items()
                     if k.startswith(pref)}
            self.set_many(items, section=prefix, commit=commit)

        else:
            self.set_many(env, commit=commit)
