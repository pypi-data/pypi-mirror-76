Getting started with CONFspirator
=================================

Installation
------------

::

    pip install confspirator

Usage
-----

First lets put together a simple ConfigGroup, and register some config values::

    # ./my_app/config/root.py
    from confspirator import groups, fields

    root_group = groups.ConfigGroup(
        "my_app", description="The root config group.")
    root_group.register_child_config(
        fields.StrConfig(
            "top_level_config",
            help_text="Some top level config on the root group.",
            default="some_default",
        )
    )

Then maybe let's make a second group, but in another file to keep things
clear::

    # ./my_app/config/sub_section.py
    from confspirator import groups, fields
    from my_app.config import root

    sub_group = groups.ConfigGroup(
        "sub_section", description="A sub group under the root group.")
    sub_group.register_child_config(
        fields.BoolConfig(
            "bool_value",
            help_text="some boolean flag value",
            default=True,
        )
    )

    root.root_group.register_child_config(sub_group)

Now we want to load in our config against this group definition and
check the values::

    # ./my_app/config/__init__.py
    import confspirator
    from my_app.config import root

    CONF = confspirator.load_file(
        root.root_group, "/etc/my_app/conf.yaml")

Assuming your config file looks like::

    # String - Some top level config on the root group.
    top_level_config: some_default
    # A sub group under the root group.
    sub_section:
      # Boolean - some boolean flag value
      bool_value: true

Then in your application code you can pull those values out and use them::

    # ./my_app/do_thing.py
    from my_app.config import CONF

    print(CONF.top_level_config)
    print(CONF.sub_section.bool_value)
