import sqlite3

# Database

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

cursor.execute(
    '''
      CREATE TABLE products(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        url TEXT UNIQUE
      )
    ''')

cursor.execute(
    '''
      CREATE TABLE prices(
        id INTEGER PRIMARY KEY,
        price TEXT,
        product_id INTEGER,
        scraped_date DATE,
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(scraped_date) REFERENCES dates(date)
      )
    ''')

cursor.execute(
    '''
      CREATE TABLE dates(
        id INTEGER PRIMARY KEY,
        date DATE DEFAULT CURRENT_DATE
      )
    ''')

cursor.execute("INSERT OR IGNORE INTO products(name, url) VALUES('AKG K702', 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=akg+k702&_sacat=0&LH_BIN=1&LH_ItemCondition=1000&_sop=12')")
cursor.execute("INSERT OR IGNORE INTO products(name, url) VALUES('AKG C214', 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=akg+c214&_sacat=0&LH_TitleDesc=0&_sop=12&LH_BIN=1&rt=nc&LH_ItemCondition=1000')")
cursor.execute("INSERT OR IGNORE INTO products(name, url) VALUES('AKG P820', 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=akg+p820&_sacat=0&LH_TitleDesc=0&LH_BIN=1&rt=nc&LH_ItemCondition=1000')")
cursor.execute("INSERT OR IGNORE INTO products(name, url) VALUES('Focurite Scarlett 2i2 3rd Gen', 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=Focusrite+Scarlett+2i2+3rd+Gen&_sacat=0&LH_TitleDesc=0&LH_BIN=1&rt=nc&LH_ItemCondition=1000')")

conn.commit()
conn.close()
