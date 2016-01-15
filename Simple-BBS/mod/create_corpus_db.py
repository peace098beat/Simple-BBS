#! coding:utf-8
"""
create_corpus_db.py
デモ用に既存サイトをスクレイピングしてデータを取得しdbに保存

モジュール
lxml, cssselect

(2016/01/13) ver0.0 たたき台を作成

Created by fifi  (2016/01/13 22:21)
"""
__version__ = '1.0'

import os
import lxml.html
from urllib2 import urlopen


def download(url, download_dir):
    """
    SAMPLE
        img_obj = urlopen(img_src)
        localfile = open('./static/updata/' + os.path.basename(img_src), 'wb')
        localfile.write(img_obj.read())
        img_obj.close()
        localfile.close()
    """
    img = urlopen(url)
    localfile = open(os.path.basename(url), 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()



def scry_okinawa_takarajima_categorypage(url):
    res = urlopen(url)
    html = res.read().decode('shift-jis')
    dom = lxml.html.fromstring(html)
    dom.make_links_absolute(url)
    dom_table_s = dom.cssselect('table')

    result = []

    for dom_table in dom_table_s:
        d = scry_oki_takara_getContent(dom_table)
        if d:
            result.append(d)

    return result


def scry_oki_takara_getContent(dom_table):

    #print '**************************************************** '
    #print  dom_table, len(dom_table)
    if len(dom_table)<2:
        #print 'This table dom is NG'
        #print ' length = ', len(dom_table)
        return False

    #print 'table dom \'s childlen'
    dom_tr1 = dom_table[0]
    dom_tr2 = dom_table[1]
    #print 'dom_tr1 =',dom_tr1
    #print 'dom_tr2 =',dom_tr2
    # 初期値準備
    title = 'Nothing'
    user_name = 'Nothing'
    img_url = 'Nothing'
    text_body = 'Nothing'

    # タイトル
    if len(dom_tr1.cssselect('b'))>0:
        title = dom_tr1.cssselect('b')[0].text_content()
        #print 'Title = ', title
    else:
        return False

    # ユーザ名
    if len(dom_tr2.cssselect('td a'))>0:
        user_name = dom_tr2.cssselect('td a')[0].text_content()
        #print 'User Name = ', user_name
    else:
        return False

    # 画像
    if len(dom_tr2.cssselect('td tr td img'))>0:
        img_url = dom_tr2.cssselect('td tr td img')[0].attrib['src']
        #print 'Image url = ', img_url
    else:
        return False

    # 本文
    if len(dom_tr2.cssselect('td tt'))>0:
        text_body = dom_tr2.cssselect('td tt')[0].text_content()
        #print 'Text Body = ', text_body
    else:
        return False

    return dict(title=title, user_name=user_name, img_url=img_url, text_body=text_body)


if __name__ == "__main__":
    url = 'http://www.dgco.jp/furima/doncyaka20/index.html'
    category = 'doncyaka20'
    category_text = '売ります　楽器　器材'
    result = scry_okinawa_takarajima_categorypage(url)
    print result