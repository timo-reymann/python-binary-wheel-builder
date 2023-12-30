from binary_wheel_builder.wrapper_templates import _preprocess


def test__preprocess():
    assert b'line one\nline two\nline three' == _preprocess('''\
    line one
    line two
    line three''')
