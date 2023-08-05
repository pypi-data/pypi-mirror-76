import toml
import yaml

from confspirator import exceptions
from confspirator import groups
from confspirator import utils


class YamlDumper(yaml.Dumper):
    """Custom dumper to deal with a weird list indentation issue.

    Remove when https://github.com/yaml/pyyaml/issues/234 is
    solved.
    """

    def increase_indent(self, flow=False, indentless=False):
        return super(YamlDumper, self).increase_indent(flow, False)


def _make_yaml_lines(field, default, depth, comment=False):
    new_lines = []
    line_prefix = "  " * depth

    field_type = field.type.__class__.__name__
    if field_type in ["Dict", "List"]:
        new_lines.append(f"{line_prefix}{field.name}:")
        line_prefix += "  "
        val = default
    else:
        val = {field.name: default}
    for line in yaml.dump(val, Dumper=YamlDumper, default_flow_style=False).split("\n"):
        if line == "":
            continue
        if comment:
            new_lines.append(f"{line_prefix}# {line}")
        else:
            new_lines.append(line_prefix + line)
    return new_lines


def _make_toml_lines(field, default, depth, comment=False):
    new_lines = []
    line_prefix = "  " * depth

    field_type = field.type.__class__.__name__
    if field_type == "Dict":
        new_lines.append(f"{line_prefix}[{field.path_str()}]")
        line_prefix += "  "

        val = {}
        pointer = val
        for name in field.path()[:-1]:
            new_dict = {}
            pointer[name] = new_dict
            pointer = new_dict
        pointer[field.name] = default
    else:
        val = {field.name: default}

    for line in toml.dumps(val).split("\n"):
        if line == "" or f"[{field.path_str()}]" in line:
            continue
        if comment:
            new_lines.append(f"{line_prefix}# {line}")
        else:
            new_lines.append(line_prefix + line)
    return new_lines


def _make_field_lines(field, depth, output_format):
    field_lines = []
    line_prefix = "  " * depth

    field_type = field.type.__class__.__name__
    if field.help_text:
        field_help_text = f"{line_prefix}# {field_type} - {field.help_text}"
    else:
        field_help_text = f"{line_prefix}# {field_type}"
    field_lines.append(field_help_text)

    if field.deprecated_for_removal:
        deprecated_text = f"{line_prefix}# DEPRECATED"
        if field.deprecated_reason:
            deprecated_text += f" - {field.deprecated_reason}"
        if field.deprecated_since:
            deprecated_text += f" - {field.deprecated_since}"
        field_lines.append(deprecated_text)

    default = ""
    if field.default is not None:
        default = field.default

    if not default and field.sample_default is not None:
        default = field.sample_default

    if field_type in ["Dict", "List"]:
        if default:
            if output_format == "yaml":
                field_lines += _make_yaml_lines(field, default, depth)
            elif output_format == "toml":
                field_lines += _make_toml_lines(field, default, depth)
        else:
            if output_format == "yaml":
                field_lines.append(f"{line_prefix}# {field.name}:")
            elif output_format == "toml":
                if field_type == "List":
                    field_lines.append(f"{line_prefix}# {field.name} = []")
                elif field_type == "Dict":
                    field_lines.append(f"{line_prefix}# [{field.path_str()}]")
    else:
        if default == "":
            if output_format == "yaml":
                field_lines.append(f"{line_prefix}# {field.name}: <your_value>")
            elif output_format == "toml":
                field_lines.append(f"{line_prefix}# {field.name} = <your_value>")
        else:
            if output_format == "yaml":
                field_lines += _make_yaml_lines(field, default, depth)
            elif output_format == "toml":
                field_lines += _make_toml_lines(field, default, depth)
    return field_lines


def _make_group_lines(group, output_format, depth=0):
    group_lines = []
    line_prefix = "  " * depth

    if group.description:
        group_lines.append(f"{line_prefix}# {group.description}")

    if output_format == "yaml":
        group_lines.append(f"{line_prefix}{group.name}:")
    elif output_format == "toml":
        group_lines.append(f"{line_prefix}[{ '.'.join(group.path()) }]")

    for child in group:
        if isinstance(child, groups.ConfigGroup):
            group_lines += _make_group_lines(child, output_format, depth=depth + 1)
        else:
            group_lines += _make_field_lines(child, depth + 1, output_format)
    return group_lines


def _create_example_lines(config_group, output_format):
    config_lines = []
    top_level_fields = False
    for child in config_group:
        if isinstance(child, groups.ConfigGroup):
            config_lines += _make_group_lines(child, output_format)
        else:
            top_level_fields = True
            config_lines += _make_field_lines(child, 0, output_format)
        # all top level configs or groups should be spaced
        config_lines.append("")
    if output_format == "toml" and top_level_fields:
        config_lines.insert(0, f"[{config_group.name}]")
    return config_lines


def create_example_config(config_group, output_file, output_format=None):
    if not isinstance(config_group, groups.ConfigGroup):
        raise exceptions.InvalidConfigClass(
            f"'{config_group}' is not a valid config class"
        )

    if not output_format:
        output_format = utils.validate_config_format(output_file.split(".")[-1])
    else:
        output_format = utils.validate_config_format(output_format)

    config_lines = _create_example_lines(config_group, output_format)

    with open(output_file, "w") as f:
        for line in config_lines:
            f.write(line)
            f.write("\n")
