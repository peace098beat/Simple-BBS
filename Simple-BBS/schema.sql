drop table if exists entries_demo;
create table entries_demo (
  id integer primary key autoincrement,
  category string not null,
  title string not null,
  text string not null,
  imagename string not null,
  username string,
  mail string,
  password string  ,
  timestamp  string DEFAULT CURRENT_TIMESTAMP
);
