# Copyright (C) 2019 Catalyst Cloud Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os

import toml
import yaml

from confspirator import constants
from confspirator import exceptions
from confspirator import base
from confspirator import groups
from confspirator import utils


def _get_nested_value(conf, path):
    """Simple recursive function to get a value down a path in a dict"""
    if conf is None:
        raise KeyError("No value in config dict.")
    if len(path) == 1:
        return conf[path[0]]
    else:
        return _get_nested_value(conf[path[0]], path[1:])


def _get_value(conf, field):
    """Get the given config field value from the conf dict

    Will attempt to get the key at the given path, or fallback
    to a deprecated path if specified.
    """
    path = field.path()
    try:
        return _get_nested_value(conf, path)
    except KeyError:
        envvar_name = field.envvar_name()
        result = os.environ.get(envvar_name, constants.DEFAULT_NONE_VALUE)

    if result == constants.DEFAULT_NONE_VALUE and field.deprecated_location:
        path = field.path(deprecated=True)
        try:
            return _get_nested_value(conf, path)
        except KeyError:
            envvar_name = field.envvar_name(deprecated=True)
            result = os.environ.get(envvar_name, constants.DEFAULT_NONE_VALUE)
    return result


def process_group(group, conf, test_mode, lazy_loading=False):
    """Process a given ConfigGroup against the conf dict into a GroupNamespace"""
    if not isinstance(group, base.BaseConfigGroup):
        raise exceptions.InvalidConfGroup("'%s' is not a valid ConfigGroup." % group)

    if group.lazy_load and not lazy_loading:
        return groups.LazyLoadedGroupNamespace(group.name, group, conf, test_mode)

    parsed_children = {}
    errors = {}
    for child in group:
        if isinstance(child, base.BaseConfigGroup):
            parsed_children[child.name] = process_group(child, conf, test_mode)
            continue

        conf_val = _get_value(conf, child)
        try:
            parsed_val = child.parse_value(conf_val, test_mode)
            parsed_children[child.name] = parsed_val
        except exceptions.InvalidConfValue as e:
            errors[child.path_str()] = e.errors

    if errors:
        raise exceptions.InvalidConfGroup(errors)

    if lazy_loading:
        return parsed_children
    return groups.GroupNamespace(group.name, parsed_children)


def load_config_dict(config_group, conf_dict, root_group_name="conf", test_mode=False):
    """Load the config group

    :param config_group: A single config group.
    :param conf_dict: The loaded dictionary of config values
    :param root_group_name: If config_groups is a list, the namespace of the
                            root wrapper group.
    :param test_mode: If test are running. Will ignore deprecation warnings
                      and ignore fields with 'required_for_tests=False'.
    """
    try:
        parsed_group = process_group(config_group, conf_dict, test_mode)
    except exceptions.InvalidConfGroup as e:
        raise exceptions.InvalidConf({config_group.name: e.errors})

    return parsed_group


def load_config_file(
    config_group,
    conf_file,
    config_format=None,
    root_group_name="conf",
    test_mode=False,
):
    """Load the config group from a file

    :param config_group: A single config group.
    :param conf_file: Config file location.
    :param config_format: The format the config file is in: yaml or toml
    :param root_group_name: If config_groups is a list, the namespace of the
                            root wrapper group.
    :param test_mode: If test are running. Will ignore deprecation warnings
                      and ignore fields with 'required_for_tests=False'.
    """

    if not config_format:
        config_format = utils.validate_config_format(conf_file.split(".")[-1])
    else:
        config_format = utils.validate_config_format(config_format)

    conf_dict = None
    if config_format == "yaml":
        with open(conf_file) as f:
            conf_dict = yaml.load(f, Loader=yaml.FullLoader)
            conf_dict = {config_group.name: conf_dict}
    elif config_format == "toml":
        conf_dict = toml.load(conf_file)

    return load_config_dict(config_group, conf_dict, root_group_name, test_mode)
