#!/usr/share/python
import re


def _find_ids(exp, path):
    count = 0
    while True:
        if exp.find('<id>') == -1:
            break

        re_id = '([^/]*-(?P<id{}>\d+))?(?P<id{}>\d+)?'.format(count, count+1)
        exp = exp.replace('<id>', re_id, 1)
        count += 2

    exp = "^(?:/[^/]+)?{}$".format(exp)

    m = re.search(exp, path)
    if not m:
        return None

    rets = []
    for i in range(0, count, 2):
        i1, i2 = i, i + 1
        id1 = m.group('id{}'.format(i1))
        id2 = m.group('id{}'.format(i2))

        rets.append(id1 if id1 else id2 if id2 else None)

    return rets


print _find_ids('/blog/<id>/post/<id>', '/blog/234/post/212')
