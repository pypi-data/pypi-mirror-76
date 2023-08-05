Configuration fields in CONFspirator
====================================

CONFspirator supports multiple different fields for configuration,
ranging from simple strings and ints, all the way to dictionaries
and lists, with some special cases like ports, hostnames, and uri's.

Options for all fields
----------------------

These options are supported for all config fields in addition to the
specific ones the field might have.

Options
+++++++

name
****
The config field's name. It is always the first parameter when defining
a config field.

help_text
*********
An explanation of how the option is used or what it is for.

default
*******
The default value of the option.

required
********
If a value must be supplied for this option and cannot be empty or blank.

test_default
************
A default for when running in test mode.

sample_default
**************
A default for sample config files.

unsafe_default (unused currently)
*********************************
If the default value must be overridden.

Once implemented will warn or raise an error when a certain flag is
given if the default value hasn't been overridden.

secret  (unused currently)
**************************
If the value should be obfuscated in log output.

Once implemented will be used to help provide information about what
values to obfuscated in logs.

deprecated_location
*******************
Deprecated dot separated location. Acts like an alias to where the config
used to be. e.g. 'service.group1.old_name'

deprecated_for_removal
**********************
Indicates whether this opt is planned for removal in a future release.

deprecated_reason
*****************
Indicates why this opt is planned for removal in a future release.
Silently ignored if deprecated_for_removal is False.

deprecated_since
****************
indicates which release this opt was deprecated in. Accepts
any string, though valid version strings are encouraged.
Silently ignored if deprecated_for_removal is False

advanced (unused currently)
***************************
A bool True/False value if this option has advanced usage
and is not normally used by the majority of users.


StrConfig
---------
Simple string based config.

Options
+++++++

name
****
The config's name.

choices  (optional)
*******************
Optional sequence of either valid values or tuples of valid
values with descriptions.

quotes  (optional)
******************
If True and string is enclosed with single or double
quotes, will strip those quotes.

regex  (optional)
*****************
Optional regular expression (string or compiled regex) that the
value must match on an unanchored search.

ignore_case  (optional)
***********************
If True case differences (uppercase vs. lowercase) between
'choices' or 'regex' will be ignored.

max_length  (optional)
**********************
If positive integer, the value must be less than or equal to
this parameter.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.StrConfig(
            "my_string_config",
            help_text="Some useful help text.",
            required=True,
            default="stuff",
        )
    )


BoolConfig
----------
Simple boolean based config.

Options
+++++++

name
****
The config's name.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.BoolConfig(
            "my_boolean_config",
            help_text="Some useful help text.",
            required=True,
            default=False,
        )
    )


IntConfig
---------
Simple int based config.

Options
+++++++

name
****
The config's name.

min  (optional)
***************
Minimum value the integer can take.

max  (optional)
***************
Maximum value the integer can take.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.IntConfig(
            "my_int_config",
            help_text="Some useful help text.",
            required=True,
            default=6,
            min=1,
            max=10,
        )
    )


FloatConfig
-----------
Simple float based config.

Options
+++++++

name
****
The config's name.

min  (optional)
***************
Minimum value the float can take.

max  (optional)
***************
Maximum value the float can take.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.FloatConfig(
            "my_float_config",
            help_text="Some useful help text.",
            required=True,
            default=6.4,
            min=1.2,
            max=10.9,
        )
    )


ListConfig
----------
A list config, with a configurable type for items.

Options
+++++++

name
****
The config's name.

item_type (optional)
********************
Type of items in the list (see :class:`confspirator.types`).
If not set will default to a list of strings.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.ListConfig(
            "my_list_config",
            help_text="Some useful help text.",
            required=True,
            default=["stuff", "things"],
        )
    )


DictConfig
----------
A dict config, with a configurable type for values.

Options
+++++++

name
****
The config's name.

value_type (optional)
*********************
Type of values in the dict (see :class:`confspirator.types`).
If not set will default to strings.

check_value_type (optional)
***************************
If value is already dict, should we check value type.

is_json (optional)
******************
If True and value is string, will parse as json.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.DictConfig(
            "my_dict_config",
            help_text="Some useful help text.",
            required=True,
            default={"stuff": "things"},
        )
    )


IPConfig
--------
IP address config.

Options
+++++++

name
****
The config's name.

version  (optional)
*******************
One of either ``4``, ``6``, or ``None`` to specify either version.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.IPConfig(
            "my_ip_config",
            help_text="Some useful help text.",
            required=True,
            default=0.0.0.0,
            version=4,
        )
    )


PortConfig
----------
Config for a TCP/IP port number.  Ports can range from 0 to 65535.

Options
+++++++

name
****
The config's name.

min  (optional)
***************
Minimum value the port can take.

max  (optional)
***************
Maximum value the port can take.

choices (optional)
******************
Sequence of valid values.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.PortConfig(
            "my_port_config",
            help_text="Some useful help text.",
            required=True,
            default=222,
            min=2000,
            max=9999,
        )
    )


HostNameConfig
--------------
Config for a hostname.  Only accepts valid hostnames.

Options
+++++++

name
****
The config's name.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.HostNameConfig(
            "my_hostname_config",
            help_text="Some useful help text.",
            required=True,
            default="prod.cluster.thing.net",
        )
    )


HostAddressConfig
-----------------
Option for either an IP or a hostname.

Options
+++++++

name
****
The config's name.

version  (optional)
*******************
One of either ``4``, ``6``, or ``None`` to specify either version.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.HostAddressConfig(
            "my_hostaddress_config",
            help_text="Some useful help text.",
            required=True,
            default="prod.cluster.thing.net",
        )
    )


URIConfig
---------
Option for either a URI.

Options
+++++++

name
****
The config's name.

max_length  (optional)
**********************
If positive integer, the value must be less than or
equal to this parameter.

schemes  (optional)
*******************
List of valid URI schemes, e.g. 'https', 'ftp', 'git'.

Example usage
+++++++++++++

::

    config_group.register_child_config(
        fields.URIConfig(
            "my_url_config",
            help_text="Some useful help text.",
            required=True,
            default="https://example.com",
            schemes["https", "http"]
        )
    )
