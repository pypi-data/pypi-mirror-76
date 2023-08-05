CONFspirator: Plot better configs!
==================================

.. image:: http://img.shields.io/pypi/v/confspirator.svg
    :target: https://pypi.python.org/pypi/confspirator

An offshoot of OpenStack's `oslo.config`_ with a focus on nested
configuration groups, and the ability to use yaml and toml instead of
flat ini files.

CONFspirator doesn't include any command-line integrations currently
so you will need to add a command to your application to export a
generated config using the built in functions.

It does have support for loading in config files, or a preloaded
config dictionary against your config group tree.

The library's focus is on in-code defaults and config field validation,
while giving you a lot of power when dealing with nesting, dynamic config
loading for plugins, and useful overlay logic.

It allows you to define sane defaults, document your config, validate
the values when loading it in, and provides useful ways of working
with that config during testing.

.. _oslo.config: https://github.com/openstack/oslo.config

Installation
------------

::

    pip install confspirator

Documentation
-------------

For more information and examples of usage `check out the docs`_.

.. _check out the docs: https://confspirator.readthedocs.io
