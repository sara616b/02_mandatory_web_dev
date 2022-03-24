DROP TABLE IF EXISTS sessions;

CREATE TABLE sessions(
    session_id             TEXT UNIQUE NOT NULL,
    PRIMARY KEY(session_id)
) WITHOUT ROWID;