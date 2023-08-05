# Copyright (C) 2020 Catalyst Cloud Ltd
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

import unittest


from confspirator import example
from confspirator import groups
from confspirator import fields


class ExampleTests(unittest.TestCase):

    maxDiff = None

    def _simple_nested_config(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group3 = groups.ConfigGroup("test3")
        config_group2.register_child_config(config_group3)
        config_group3.register_child_config(
            fields.StrConfig("some_value", required=True)
        )
        return config_group

    def _complex_nested_config(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group3 = groups.ConfigGroup("test3")
        config_group2.register_child_config(config_group3)
        config_group3.register_child_config(
            fields.StrConfig(
                "some_value",
                help_text="help text for some_value",
                required=True,
                default="stuff",
            )
        )

        config_group2.register_child_config(
            fields.DictConfig(
                "some_dict",
                help_text="a dict field with a large default.",
                default={
                    "level1": {
                        "level2": {
                            "level3": {"level4": {"some_bool": False, "some_int": 5}}
                        }
                    },
                    "level1a": {"level2a": {"level3a": {"stuff": "things"}}},
                },
            )
        )
        config_group2.register_child_config(
            fields.DictConfig(
                "some_dict_2",
                help_text="a dict to test a weird circular export edge case",
                default={"l1": {"l2": {"l3": {"l4": {}}}}},
            )
        )
        return config_group

    def _all_fields_config(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group2.register_child_config(
            fields.StrConfig(
                "some_string", help_text="help text for some_string", default="stuff",
            )
        )
        config_group2.register_child_config(fields.IntConfig("some_int", default=991,))
        config_group2.register_child_config(
            fields.FloatConfig("some_float", default=9.81,)
        )
        config_group2.register_child_config(
            fields.BoolConfig(
                "is_boolean", help_text="boolean field help text", default=True,
            )
        )
        config_group2.register_child_config(
            fields.ListConfig(
                "some_list",
                help_text="List things.",
                default=["thing1", "thing2", "thing3"],
            )
        )
        config_group2.register_child_config(
            fields.DictConfig(
                "some_dict",
                help_text="a dict field help text",
                default={"level1": {"level2": {"level3": {"level4": {}}}}},
            )
        )
        config_group2.register_child_config(
            fields.IPConfig("some_ip", default="0.0.0.1")
        )
        config_group2.register_child_config(
            fields.PortConfig("some_port", default="7728")
        )
        config_group2.register_child_config(
            fields.HostNameConfig("some_host", default="place.example.org")
        )
        config_group2.register_child_config(
            fields.HostAddressConfig("some_hostaddress", default="place.example.org")
        )
        config_group2.register_child_config(
            fields.URIConfig("some_uri", default="https://place.example.org")
        )
        return config_group

    def _top_level_config(self):
        """Config fields at the top level
        """
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group.register_child_config(
            fields.StrConfig("some_value", default="test")
        )
        config_group2.register_child_config(
            fields.StrConfig("some_value2", default="test2")
        )
        return config_group

    def test_example_config_simple_nested_yaml(self):
        config_group = self._simple_nested_config()

        expected_lines = [
            "test2:",
            "  test3:",
            "    # String",
            "    # some_value: <your_value>",
            "",
        ]
        config_lines = example._create_example_lines(config_group, "yaml")
        self.assertEqual(config_lines, expected_lines)

    def test_example_config_simple_nested_toml(self):
        config_group = self._simple_nested_config()

        expected_lines = [
            "[test.test2]",
            "  [test.test2.test3]",
            "    # String",
            "    # some_value = <your_value>",
            "",
        ]
        config_lines = example._create_example_lines(config_group, "toml")
        self.assertEqual(config_lines, expected_lines)

    def test_example_config_complex_nested_yaml(self):
        config_group = self._complex_nested_config()

        expected_lines = [
            "test2:",
            "  # Dict - a dict field with a large default.",
            "  some_dict:",
            "    level1:",
            "      level2:",
            "        level3:",
            "          level4:",
            "            some_bool: false",
            "            some_int: 5",
            "    level1a:",
            "      level2a:",
            "        level3a:",
            "          stuff: things",
            "  # Dict - a dict to test a weird circular export edge case",
            "  some_dict_2:",
            "    l1:",
            "      l2:",
            "        l3:",
            "          l4: {}",
            "  test3:",
            "    # String - help text for some_value",
            "    some_value: stuff",
            "",
        ]
        config_lines = example._create_example_lines(config_group, "yaml")
        self.assertEqual(config_lines, expected_lines)

    def test_example_config_complex_nested_toml(self):
        config_group = self._complex_nested_config()

        expected_lines = [
            "[test.test2]",
            "  # Dict - a dict field with a large default.",
            "  [test.test2.some_dict]",
            "    [test.test2.some_dict.level1a.level2a.level3a]",
            '    stuff = "things"',
            "    [test.test2.some_dict.level1.level2.level3.level4]",
            "    some_bool = false",
            "    some_int = 5",
            "  # Dict - a dict to test a weird circular export edge case",
            "  [test.test2.some_dict_2]",
            "    [test.test2.some_dict_2.l1.l2.l3.l4]",
            "  [test.test2.test3]",
            "    # String - help text for some_value",
            '    some_value = "stuff"',
            "",
        ]
        config_lines = example._create_example_lines(config_group, "toml")
        self.assertEqual(config_lines, expected_lines)

    def test_example_config_all_fields_yaml(self):
        config_group = self._all_fields_config()

        expected_lines = [
            "test2:",
            "  # String - help text for some_string",
            "  some_string: stuff",
            "  # Integer",
            "  some_int: 991",
            "  # Float",
            "  some_float: 9.81",
            "  # Boolean - boolean field help text",
            "  is_boolean: true",
            "  # List - List things.",
            "  some_list:",
            "  - thing1",
            "  - thing2",
            "  - thing3",
            "  # Dict - a dict field help text",
            "  some_dict:",
            "    level1:",
            "      level2:",
            "        level3:",
            "          level4: {}",
            "  # IPAddress",
            "  some_ip: 0.0.0.1",
            "  # Port",
            "  some_port: '7728'",
            "  # Hostname",
            "  some_host: place.example.org",
            "  # HostAddress",
            "  some_hostaddress: place.example.org",
            "  # URI",
            "  some_uri: https://place.example.org",
            "",
        ]
        config_lines = example._create_example_lines(config_group, "yaml")
        self.assertEqual(config_lines, expected_lines)

    def test_example_config_all_fields_toml(self):
        config_group = self._all_fields_config()

        expected_lines = [
            "[test.test2]",
            "  # String - help text for some_string",
            '  some_string = "stuff"',
            "  # Integer",
            "  some_int = 991",
            "  # Float",
            "  some_float = 9.81",
            "  # Boolean - boolean field help text",
            "  is_boolean = true",
            "  # List - List things.",
            '  some_list = [ "thing1", "thing2", "thing3",]',
            "  # Dict - a dict field help text",
            "  [test.test2.some_dict]",
            "    [test.test2.some_dict.level1.level2.level3.level4]",
            "  # IPAddress",
            '  some_ip = "0.0.0.1"',
            "  # Port",
            '  some_port = "7728"',
            "  # Hostname",
            '  some_host = "place.example.org"',
            "  # HostAddress",
            '  some_hostaddress = "place.example.org"',
            "  # URI",
            '  some_uri = "https://place.example.org"',
            "",
        ]
        self.maxDiff = None
        config_lines = example._create_example_lines(config_group, "toml")
        self.assertEqual(config_lines, expected_lines)

    def test_example_config_top_level_fields_yaml(self):
        config_group = self._top_level_config()

        expected_lines = [
            "# String",
            "some_value: test",
            "",
            "test2:",
            "  # String",
            "  some_value2: test2",
            "",
        ]

        config_lines = example._create_example_lines(config_group, "yaml")
        self.assertEqual(config_lines, expected_lines)

    def test_example_config_top_level_fields_toml(self):
        config_group = self._top_level_config()

        expected_lines = [
            "[test]",
            "# String",
            'some_value = "test"',
            "",
            "[test.test2]",
            "  # String",
            '  some_value2 = "test2"',
            "",
        ]
        config_lines = example._create_example_lines(config_group, "toml")
        self.assertEqual(config_lines, expected_lines)

    def test_example_config_toml_field_ordering(self):
        """Test that output format always places fields before groups

        Fields in a given group need to be placed before any subgroups
        else toml will read them as included in the next group.

        Yaml this isn't an issue since indentation solves it, but for toml
        we need to ensure fields as written down before a subgroup.
        """
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group2a = groups.ConfigGroup("test2a")
        config_group.register_child_config(config_group2a)
        config_group3 = groups.ConfigGroup("test3")
        config_group2.register_child_config(config_group3)
        config_group.register_child_config(
            fields.StrConfig("some_value", required=True)
        )
        config_group.register_child_config(fields.IntConfig("some_int", required=True))
        config_group2.register_child_config(
            fields.StrConfig("some_value2", required=True)
        )
        config_group2a.register_child_config(
            fields.StrConfig("some_value2a", required=True)
        )

        expected_lines = [
            "[test]",
            "# String",
            "# some_value = <your_value>",
            "",
            "# Integer",
            "# some_int = <your_value>",
            "",
            "[test.test2]",
            "  # String",
            "  # some_value2 = <your_value>",
            "  [test.test2.test3]",
            "",
            "[test.test2a]",
            "  # String",
            "  # some_value2a = <your_value>",
            "",
        ]
        config_lines = example._create_example_lines(config_group, "toml")
        self.assertEqual(config_lines, expected_lines)
