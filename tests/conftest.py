import pytest
from compressor import FileManager, NoCompressionCompressor


@pytest.fixture
def file_manager(tmp_path):
    file_path = tmp_path / "example.csv"
    file_path.write_text("key1,value1\nkey2,value2\n")
    return FileManager(file_path, NoCompressionCompressor)
