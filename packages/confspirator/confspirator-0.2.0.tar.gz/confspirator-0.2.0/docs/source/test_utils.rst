CONFspirator in your unit tests
===============================

You often need ways to override config when running tests,
so CONFspirator provides some powerful ways to do that even
for the most complicated of nested configs.

Setting test defaults
---------------------

The first smart thing to do is set the ``test_default`` value on
a given config field for something you want to be a global test
default value. This is useful for values you rarely need to
change, and this means you can put your test defaults in the
same places you define you config and put your actual defaults.

An example of this might be::

    config_group.register_child_config(
        fields.StrConfig(
            "my_string_config",
            help_text="Some useful help text.",
            required=True,
            default="stuff",
            test_default="test_specific_stuff",
        )
    )

To ensure CONFspirator uses the ``test_default`` you will need to put it
into ``test_mode`` when running the load config functions::

    CONF = confspirator.load_file(
        config_group, "/etc/my_app/conf.yaml", test_mode=True)

That does mean you will need some way to decide when loading config
if your application is running in ``test_mode``. This will vary depending
on your framework, or unit testing tools, but as an example, in Django
you could do it as follows::

    test_mode = False
    if "test" in sys.argv:
        test_mode = True

    CONF = confspirator.load_file(
        config_group, "/etc/my_app/conf.yaml", test_mode=test_mode)

Overriding config for test cases
--------------------------------

Often in unit or functional testing you need ways to override config
for the duration of a test, a whole set of tests, or even in different
phases of a test.

As such CONFspirator provides an all powerful ``modify_conf`` function
that alows you to selectively alter your config entity for the needed
scope.

.. note::

    ``modify_conf`` assumes your test case classes inherit from
    ``unittest.TestCase``. If they do not, then this will not work.

A simple example::

    import confspirator

    from my_app.config import CONF


    @confspirator.modify_conf(
        CONF,
        {
            "my_app.top_level_config": [
                {"operation": "override", "value": "a new value"}
            ],
        }
    )
    class BasicTests(TestCase):

        def test_top_level_config(self):
            self.assertEqual(CONF.top_level_config, "a new value")

It can also be used to decorate a single test function::

    import confspirator

    from my_app.config import CONF


    class BasicTests(TestCase):

        @confspirator.modify_conf(
            CONF,
            {
                "my_app.top_level_config": [
                    {"operation": "override", "value": "a new value"}
                ],
            }
        )
        def test_top_level_config(self):
            self.assertEqual(CONF.top_level_config, "a new value")

Or even a section when using the ``with`` keyword::

    import confspirator

    from my_app.config import CONF


    class BasicTests(TestCase):
        def test_top_level_config(self):
            with confspirator.modify_conf(
                CONF,
                {
                    "my_app.top_level_config": [
                        {"operation": "override", "value": "a new value"}
                    ],
                },
            ):
                self.assertEqual(CONF.top_level_config, "a new value")

parameters for modify_conf
++++++++++++++++++++++++++

``modify_conf`` takes two argument which can be used positionally, or
as keywords.

conf
****

This should be the loaded config entity and will be either an
instance of ``GroupNamespace`` or in advanced cases
``LazyLoadedGroupNamespace``.

operations
**********

This is a dictionary of config values as dot separated paths to a list
of operations.

It is possible to alter multiple config values at the same time, and
run multiple operations on each. Operations will run in the order
supplied and can be chained together (e.g. add a value to the start
and end of a list).

Here is what a more complex example may look like::

    operations={
        "my_app.api_settings.item_list_option": [
            {"operation": "remove", "value": "option1"},
            {"operation": "append", "value": "option15"},
        ],
        "my_app.api_settings.boolean_flag_option": [
            {"operation": "override", "value": False},
        ],
    }

Available operations per config type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- value:
    - override
- list:
    - override
    - preprend
    - append
    - remove
- dict:
    - override
    - update
    - delete
    - overlay
- GroupNamespace:
    - override
    - overlay

Overlay is essential a dict merge, where any keys present in the
overlaying dictionay will be inserted or will override the ones
in the target.
