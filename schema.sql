DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,  -- 名前カラムを追加
    text TEXT NOT NULL,
    created_at DATETIME NOT NULL
);
