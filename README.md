# SQLiteの使い方

# IDの自動インクリメント
    # AUTOINCREMENT削除されても同じIDは使われない
    ID INTEGER PRIMARY KEY AUTOINCREMENT,

# 自動でタイムスタンプを追加する
CREATE TABLE GPS_Logger (
    ID INTEGER PRIMARY KEY,
    t TIMESTAMP CURRENT_TIMESTAMP  <-INSERT時に値を指定しなければTIMESTAMPにはタイムスタンプが自動で指定
    t TIMESTAMP DEFAULT (DATETIME(‘now’,’localtime’)) <-デフォルトTimeZoneをJST
    )

CURRENT_TIME         HH:MM:SS
CURRENT_DATE         YYYY-MM-DD
CURRENT_TIMESTAMP    YYYY-MM-DD HH:MM:SS