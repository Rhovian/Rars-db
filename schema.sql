CREATE TABLE BOXES (
  TR_ID SERIAL NOT NULL PRIMARY KEY,    /* Table row ID */
  TS NUMERIC, 
  BOX_ID TEXT NOT NULL UNIQUE,          /* Need to find out string length */
  CABINET_ID TEXT UNIQUE
);

CREATE TABLE films (
  TR_ID SERIAL NOT NULL PRIMARY KEY,
  FILM_ID TEXT,                         /* Need to find out string length */
  TS NUMERIC,
  LOCATION TEXT,                        /* 100 slots per box */
  BOX_ID TEXT,
  CONSTRAINT box_constraint
  FOREIGN KEY (BOX_ID)
  REFERENCES BOXES (BOX_ID)
);