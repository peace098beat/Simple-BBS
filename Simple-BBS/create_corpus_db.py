#! coding:utf-8
"""
create_corpus_db.py
デモ用に既存サイトをスクレイピングしてデータを取得しdbに保存

(2016/01/13) ver0.0 たたき台を作成

Created by fifi  (2016/01/13 22:21)
"""
__version__ = '0.0'

import lxml.html
from urllib2 import urlopen


def main():
    # できた!

    url = 'http://www.dgco.jp/furima/doncyaka20/index.html'
    res = urlopen(url)
    html = res.read().decode('shift-jis')
    root = lxml.html.fromstring(html)
    # タイトル
    elem = root.cssselect('table  b')
    for p in elem:
        s = p.text_content()
        print s
    # 本文
    elem = root.cssselect('table  table tt')
    for p in elem:
        s = p.text_content()
        print s
    # 画像名前
    elem = root.cssselect('table tr td table tr td')
    for e in elem:
        img = e.xpath('//img')
        for i in img:
            print i.attrib['src']


if __name__ == "__main__":
    main()
