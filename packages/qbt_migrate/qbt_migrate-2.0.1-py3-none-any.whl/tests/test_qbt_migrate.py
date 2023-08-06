from qbt_migrate import QBTBatchMove, FastResume, valid_path, convert_slashes


def test_convert_slashes():
    path = 'C:\\This\\is\\a\\windows\\path'
    assert convert_slashes(path, 'Windows') == path
    assert convert_slashes(path, 'Linux') == path.replace('\\', '/')

    path = '/this/is/a/nix/path'
    assert convert_slashes(path, 'Linux') == path
    assert convert_slashes(path, 'Windows') == path.replace('/', '\\')
