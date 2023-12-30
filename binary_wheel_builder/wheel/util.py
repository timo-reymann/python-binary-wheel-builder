from email.message import EmailMessage


def generate_wheel_file(tag: str):
    return generate_metafile_content({
        'Wheel-Version': '1.0',
        'Generator': 'binary-wheel-builder',
        'Root-Is-Purelib': 'false',
        'Tag': tag,
    })


def generate_metadata_file(name: str, version: str, description: str, **metadata):
    return generate_metafile_content({
        'Metadata-Version': '2.1',
        'Name': name,
        'Version': version,
        **metadata,
    }, description)


def generate_metafile_content(headers: dict[str, str], payload=None) -> bytes:
    msg = EmailMessage()
    for name, value in headers.items():
        if isinstance(value, list):
            for value_part in value:
                msg[name] = value_part
        elif isinstance(value, dict):
            for key, val in value.items():
                msg[name] = f'{key}, {val}'
        else:
            msg[name] = value
    if payload:
        msg.set_payload(payload)
    return str(msg).encode("utf8")
