import dataclasses
import importlib
from typing import Generator, Tuple

import yaml

from cli_wheel_builder import Wheel, WheelSource, WheelPlatformIdentifier
from cli_wheel_builder.api import well_known_platforms


def validate_wheel_data(data):
    required_fields = [
        "package",
        "executable",
        "name",
        "version",
        "source",
        "platforms"
    ]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    allowed_fields = set([field.name for field in list(dataclasses.fields(Wheel))])
    unknown_fields = set(data.keys()) - allowed_fields

    if unknown_fields:
        raise ValueError(f"Unknown fields found: {', '.join(unknown_fields)}")

    return data


def iterate_mapping_node(
        loader: yaml.SafeLoader,
        node: yaml.nodes.MappingNode
) -> Generator[Tuple[str, any], None, None]:
    for mapping_node in node.value:
        key_node, value_node = mapping_node
        yield key_node.value, loader.construct_object(value_node, True)


def construct_well_known_platform(_: yaml.SafeLoader, node: yaml.nodes.ScalarNode) -> WheelPlatformIdentifier:
    name = node.value
    if not hasattr(well_known_platforms, name):
        raise yaml.constructor.ConstructorError(None, None,
                                                "could not determine well known platform with name %s" % node.value,
                                                node.start_mark)
    return getattr(well_known_platforms, name)


def construct_wheel_source(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> WheelSource:
    kwargs = {}
    implementation_class = ""
    for key, val in iterate_mapping_node(loader, node):
        if key == "implementation":
            implementation_class = val
            continue

        kwargs[key] = val

    if implementation_class.strip() == "":
        raise yaml.constructor.ConstructorError(None, None,
                                                "No wheel source implementation specified in tag %r" % node.tag,
                                                node.start_mark)

    module_name, class_name = implementation_class.rsplit('.', 1)
    try:
        module = importlib.import_module(module_name)
        source_impl = getattr(module, class_name)
    except:
        raise yaml.constructor.ConstructorError(None, None,
                                                "Wheel source implementation for tag %r could not be instantiated" % node.tag,
                                                node.start_mark)
    return source_impl(**kwargs)


def yaml_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!WellknownPlatform", construct_well_known_platform)
    loader.add_constructor("!WheelSource", construct_wheel_source)
    return loader


# Function to load YAML file and create Wheel instance
def load_wheel_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml_loader())
        if data is None:
            raise ValueError("Config file can not be empty")
        validated_data = validate_wheel_data(data)
        return Wheel(**validated_data)
