from gmsrq.gmquests import find_format_tag, FormatToken


def test_find_format_tag():
    tag = find_format_tag('<format=center,   40>body</format>')
    assert tag == FormatToken(beginIdx=0, endIdx=34, body='body',
                              padding='center', paddingSize=40)

    tag = find_format_tag('<format=center, 41>body</format>')
    assert tag == FormatToken(beginIdx=0, endIdx=32, body='body',
                              padding='center', paddingSize=41)

    tag = find_format_tag('<format=left,20>body</format>')
    assert tag == FormatToken(beginIdx=0, endIdx=29, body='body',
                              padding='left', paddingSize=20)

    tag = find_format_tag('no format')
    assert not tag
