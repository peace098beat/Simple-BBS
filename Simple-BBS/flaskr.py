# -*- coding: utf-8 -*-
"""
flaskr.py
シンプル掲示板

使い方
python flaskr.py

Tips
app.run(debug=True) Trueにしてると、自動更新とエラー表示(たぶん)

参考
[Flaskで画像UPLOAD] https://github.com/peace098beat/flask-fileupload-sample

(2016/01/12) ver0.0
"""
__version__ = 0.1
__app_name__ = 'flaskr app'
# TODO:画像のアップロードと保存

# all the imports
import sqlite3
from contextlib import closing
# all the imports
from flask import Flask, request, session, g, redirect
from flask import url_for, abort, render_template, flash

# 各種設定情報を記述
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# サイトコンテンツ用の初期値
# =========================
CATEGORIES = [dict(name="car", text=u"車"),
              dict(name="accessories", text=u"アクセサリー"),
              dict(name="audio", text=u"音楽・機材・楽器"),
              dict(name="game", text=u"ゲーム／本体・ソフト/玩具")]

# アプリ生成
app = Flask(__name__)

# app.config.from_object()
# from_object() では、与えられたオブジェクトの内で 大文字の変数をすべて取得します。大変便利ですね。
# 上記大文字の変数をすべてConfigに格納している。(便利)
# 今回は flask.py ファイル自体を 渡していますが、コンフィグを別ファイルに書いた場合には、適宜書き換えてください。
# TODO:Configを別ファイルに移動
app.config.from_object(__name__)

# app.config.from_envvar
# 環境変数から設定を引き継ぐことも出来ます from_envvar()
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# DB周り
# DB接続
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


# DBの初期化
def init_db():
    print 'init_db()'
    print '__name__'
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


#
# flaskは、DB処理の前後で別処理をするには以下のようなデコレータを利用することで可能になります。
# before_request() もしくわ after_request()
#
# リクエストに対する前処理
# リクエストがきたらまずDBへ接続する。
@app.before_request
def before_request():
    print '__before_request()__'
    g.db = connect_db()


# リクエストに対する後処理
@app.teardown_request
def teardown_request(exception):
    print __name__
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# View
# DBのエントリー一覧ページ
@app.route('/show_entries')
def show_entries():
    """テンプレート(使ってない)
    DBにアクセスしエントリを取得。エントリを辞書型でリストに格納。HTMLレンダリング
    """
    # DBからエントリを取得する
    # TODO:(削除予定:次verで削除) DBアクセスのSQLに脆弱性
    # cur = g.db.execute('select title, text from entries order by id desc')
    # 複数のエントリの整形
    # entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    # 取得したエントリを使ってhtmlをレンダリング
    return render_template('show_entries.html', entries=entries)


@app.route('/category/<category_name>')
def show_category_page(category_name):
    """
    カテゴリページのview
    :param category_name: カテゴリを表すname (例:car, animal)
    """
    # DBからエントリを取得する
    cur = g.db.execute('select title, text, category from entries order by id desc')

    # 複数のエントリの整形
    # TODO:カテゴリ別にDBから取得するSQLを作り、特定カテゴリだけデータを取得する.(とりあえずforで回避)
    entries = [dict(title=row[0], text=row[1], category=row[2]) for row in cur.fetchall() if row[2] == category_name]

    # カテゴリを検索(category_nameが格納されている辞書を取得するため)
    for search_category in CATEGORIES:
        if search_category["name"] == category_name:
            print category_name, search_category["name"], search_category["text"]
            category = search_category

    # 念のためflushで通知
    flash(u'show_category_pageがひらかれました')

    # 取得したエントリを使ってhtmlをレンダリング
    return render_template('category_page.html', entries=entries, category=category)


@app.route('/')
def top_page():
    """topページのVIEW"""
    # カテゴリ一覧の辞書を取得
    categories = CATEGORIES
    # 念のためflushで通知
    flash(u'/top.htmlがひらかれました')
    # 取得したエントリを使ってhtmlをレンダリング
    return render_template('top.html', categories=categories)


# エントリー追加
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text, category) values (?, ?, ?)',
                 [request.form['title'], request.form['text'], request.form['category']])
    g.db.commit()
    flash(u'新しいエントリーが追加されました')

    # 画像の保存
    if request.method == 'POST':
        f = request.files['file']
        f.save('./image/' + f.filename)
        flash(u'%sをuploadしました'%f.filename)
    # TODO: 保存先の仕様を決定
    # TODO: 画像のプレビューを表示

    # redirectとrender_templateの違い。おそらくPOSTのデータがクリアされている
    return redirect(url_for('show_category_page', category_name=request.form['category']))


#
# ログインとログアウト
# 以下のファンクションは、ユーザーのログインとログアウト時に使います。
# ログインには、ユーザーネームとパスワードを利用して行ない、session内に logged_in のキーで設定がセットされます。
# もし、ログイン済みの場合は、Keyは True がセットされている ので、ユーザは show_entries ページにリダイレクトされます。
# 追加メッセージで、ユーザに ログインが成功した事が通知され、もしエラーが発生した場合は、ユーザに再度入力を求める

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # POSTのみ利用可能
    if request.method == 'POST':
        # ユーザネームの照合(照合先は先に設定した設定変数)
        if request.form['username'] != app.config['USERNAME']:
            error = u'ユーザ名が間違っています'
        # パスワードの照合(照合先は先に設定した設定変数)
        elif request.form['password'] != app.config['PASSWORD']:
            error = u'パスワードが間違っています'
        # 照合成功!
        else:
            # ログインセッションをTrueにする。これが鍵になる。
            session['logged_in'] = True
            flash(u'ログインしました')
            # ログインできたら
            return redirect(url_for('show_entries'))
    # ログイン失敗時に再度login.htmlへリダイレクトされる
    return render_template('login.html', error=error)


#
# ログアウト処理は、sessionからkeyを削除します。
# また、以下のような方法でもログアウト処理を行えます。
# pop() を 使用することでsession内からkeyを削除することが出来ます。
# 未ログイン状態でも 以下のメソッドは使用可能なので、ログイン状態チェックすることなく利用する事が 可能です。
#
# ログアウト
@app.route('/logout')
def logout():
    # pop() を 使用することでsession内からkeyを削除することが出来ます。
    session.pop('logged_in', None)
    flash(u'ログアウトしました')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    print __name__
    init_db()
    # app.run(debug=False)
    app.run(debug=True)