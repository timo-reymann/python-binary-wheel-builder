import importlib
from pathlib import Path
from collections.abc import Generator

import yaml

from binary_wheel_builder import WheelSource, WheelPlatformIdentifier
from binary_wheel_builder.api import well_known_platforms


def _iterate_mapping_node(
        loader: yaml.SafeLoader,
        node: yaml.nodes.MappingNode
) -> Generator[tuple[str, any], None, None]:
    for mapping_node in node.value:
        key_node, value_node = mapping_node
        yield key_node.value, loader.construct_object(value_node, True)


def _construct_well_known_platform(_: yaml.SafeLoader, node: yaml.nodes.ScalarNode) -> WheelPlatformIdentifier:
    name = node.value
    if not hasattr(well_known_platforms, name):
        raise yaml.constructor.ConstructorError(None, None,
                                                "could not determine well known platform with name %s" % node.value,
                                                node.start_mark)
    return getattr(well_known_platforms, name)


def _construct_wheel_source(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> WheelSource:
    kwargs = {}
    implementation_class = ""
    for key, val in _iterate_mapping_node(loader, node):
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


def _construct_wheel_platform_identifier(loader: yaml.SafeLoader,
                                         node: yaml.nodes.MappingNode) -> WheelPlatformIdentifier:
    kwargs = {}

    for key, val in _iterate_mapping_node(loader, node):
        if key not in ['platform', 'python_tag', 'abi_tag']:
            raise yaml.constructor.ConstructorError(None, None,
                                                    "Unsupported argument %s with value '%s'" % (key, val),
                                                    node.start_mark)
        kwargs[key] = val

    return WheelPlatformIdentifier(**kwargs)


class YamlSafeLoaderWithFileContext(yaml.SafeLoader):
    file_path: Path


def _construct_file_content(loader: YamlSafeLoaderWithFileContext, node: yaml.nodes.ScalarNode) -> str:
    file_path = Path(loader.file_path.parent, node.value)
    if not file_path.exists() or file_path.is_dir():
        raise yaml.constructor.ConstructorError(None, None,
                                                "%s does not resolve to a file" % str(file_path),
                                                node.start_mark)
    return file_path.read_text()


def _construct_env_var_content(_: YamlSafeLoaderWithFileContext, node: yaml.nodes.ScalarNode) -> str:
    from os import environ
    env_var = node.value
    val = environ.get(env_var, None)
    if val is None:
        raise yaml.constructor.ConstructorError(None, None,
                                                "Environment variable %s not set" % env_var,
                                                node.start_mark)
    return val


def _yaml_loader(file_path):
    loader = YamlSafeLoaderWithFileContext
    loader.add_constructor("!WellknownPlatform", _construct_well_known_platform)
    loader.add_constructor("!WheelSource", _construct_wheel_source)
    loader.add_constructor("!WheelPlatform", _construct_wheel_platform_identifier)
    loader.add_constructor("!FileContent", _construct_file_content)
    loader.add_constructor("!Env", _construct_env_var_content)
    loader.file_path = file_path
    return loader


def load_file(file_path: Path) -> dict:
    with file_path.open("r") as file:
        data = load_stream(file, file_path)
    return data


def load_stream(stream, file_path: Path) -> dict:
    return yaml.load(stream, Loader=_yaml_loader(file_path))
