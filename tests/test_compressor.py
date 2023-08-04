def test_read(file_manager):
    expected_data = '[{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]'
    assert file_manager.read() == expected_data


def test_write(file_manager, tmp_path):
    data = '[{"key": "key3", "value": "value3"}]'
    output_file = tmp_path / "output_file.csv"
    file_manager.write(output_file, data)
    assert output_file.read_text() == data
