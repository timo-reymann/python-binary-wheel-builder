from binary_wheel_builder.wheel.util import generate_wheel_file, generate_metadata_file


def test_generate_wheel_file():
    content = generate_wheel_file("tag")
    assert (b'Wheel-Version: 1.0\n'
            b'Generator: binary-wheel-builder\n'
            b'Root-Is-Purelib: false\n'
            b'Tag: tag\n'
            b'\n') == content


def test_generate_metadata_file():
    content = generate_metadata_file(
        "name",
        "1.0.0",
        "Description",
        **{
            'Meta Key': 'Meta val',
            'Meta List': ['Meta val 1', 'Meta val 2'],
            'Meta dict': {'Key': 'Val'}
        })
    assert (b'Metadata-Version: 2.1\n'
            b'Name: name\n'
            b'Version: 1.0.0\n'
            b'Meta Key: Meta val\n'
            b'Meta List: Meta val 1\n'
            b'Meta List: Meta val 2\n'
            b'Meta dict: Key, Val\n'
            b'\n'
            b'Description') == content
