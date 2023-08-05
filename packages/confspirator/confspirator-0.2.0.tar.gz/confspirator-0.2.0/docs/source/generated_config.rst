Example config generation
=========================

CONFspirator supports generated config files from the built
config tree. These will populate all the fields, and if a
default value is supplied will put that in place.

To use this functionality you must supply your root config group,
and call the function with a file location. CONFspirator does not
supply any CLI support for this, so you will want to build a command
into your application or project to import your root config group,
and call the generation function.

Assuming the config group as shown in the getting started page::

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

You would call the generation logic as follows::

    # ./my_app/commands.py

    import confspirator
    from my_app.config import root


    def create_config():
        confspirator.create_example_config(
            root.root_group, "conf.yaml")

This would produce a yaml config example that looks like the following::

    # String - Some top level config on the root group.
    top_level_config: some_default
    # A sub group under the root group.
    sub_section:
      # Boolean - some boolean flag value
      bool_value: true

Alternatively if you wanted ``toml`` instead, you can simply change the
file extension and the exporter will pick that up. Or if you want to use
an extension other than ``yaml`` or ``toml`` you can explicitly set
``output_format`` to either ``yaml`` or ``toml``, and the file extension
will be ignored::

    confspirator.create_example_config(
        root.root_group, "my_app.conf", output_format="toml")

In any case, if by extension or explicit output format ``toml`` is set,
your generated example config will look as follows::

    [my_app]
    # String - Some top level config on the root group.
    top_level_config = "some_default"

    # A sub group under the root group.
    [my_app.sub_section]
      # Boolean - some boolean flag value
      bool_value = true

For complicated nested configs yaml tends to be easier to deal with,
but for people with a preference for ``ini`` style configs toml does
provide a good option that still allows nesting.
