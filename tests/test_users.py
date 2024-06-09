from gmsrq.gmusers import is_valid_name


def test_is_invalid():
    assert not is_valid_name('')
    assert not is_valid_name('q' * 128)
    assert not is_valid_name('qwe\n')
    assert not is_valid_name('qwe\r')
    assert not is_valid_name('qwe```')
    assert is_valid_name('qwe')
    assert is_valid_name('q' * 127)
