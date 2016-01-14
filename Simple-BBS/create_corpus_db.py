#! coding:utf-8
"""
create_corpus_db.py
デモ用に既存サイトをスクレイピングしてデータを取得しdbに保存

モジュール
lxml, cssselect

(2016/01/13) ver0.0 たたき台を作成

Created by fifi  (2016/01/13 22:21)
"""
__version__ = '0.0'

import os
import lxml.html
from urllib2 import urlopen

def download(url, download_dir):
    img = urlopen(url)
    localfile = open(os.path.basename(url), 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()

def main():

    url = 'http://www.dgco.jp/furima/doncyaka20/index.html'
    res = urlopen(url)
    html = res.read().decode('shift-jis')
    dom = lxml.html.fromstring(html)
    dom.make_links_absolute(url)


    # タイトル
    elem = dom.cssselect('table  b')
    for p in elem:
        s = p.text_content()
        # print s

    # 本文
    elem = dom.cssselect('table table tt')
    for p in elem:
        s = p.text_content()
        # print s

    # 画像名前
    elem = dom.cssselect('table table img')
    for e in elem:
        img = e.xpath('//img')
        for i in img:
            img_src = i.attrib['src']
            print img_src
            img_obj = urlopen(img_src)
            localfile = open('./static/updata/'+os.path.basename(img_src), 'wb')
            localfile.write(img_obj.read())
            img_obj.close()
            localfile.close()





if __name__ == "__main__":
    main()
