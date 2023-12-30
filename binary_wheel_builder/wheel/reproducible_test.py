import hashlib
import os
import tempfile
from pathlib import Path

from binary_wheel_builder.api.meta import WheelFileEntry
from binary_wheel_builder.wheel.reproducible import ReproducibleWheelFile


def test_reproducible_wheel_zipfile():
    f = tempfile.mkdtemp() + "/wheel-0.0.1-py3-none-any.whl"
    zip = ReproducibleWheelFile(Path(f),"w")
    zip.write_content_file(WheelFileEntry(
        path="test.txt",
        content="Hello World".encode("utf-8"),
        permissions=0o644
    ))
    zip.close()
    with open(f,"rb") as fp:
        actual_hash = hashlib.sha256(fp.read()).hexdigest()
    os.unlink(f)
    assert "f4873928fe1f041339ee38dacb30af0e4f1c3b5824d00316352d58679b42901a" == actual_hash
