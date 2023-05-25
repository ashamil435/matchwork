import duckdb


class ParserPipeline:
    def __init__(self) -> None:
        self.con = duckdb.connect(database='./../database.duckdb', read_only=False)
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS projects(
                        id UINTEGER PRIMARY KEY,
                        link VARCHAR NOT NULL,
                        name VARCHAR NOT NULL,
                        price VARCHAR NOT NULL,
                        tags VARCHAR DEFAULT NULL,
                        time TIME NOT NULL,
                        date DATE NOT NULL,
                        views UTINYINT NOT NULL,
                        responses UTINYINT NOT NULL,
                        description VARCHAR NOT NULL,
                        description_links VARCHAR[] DEFAULT NULL,
                        user_files VARCHAR[] DEFAULT NULL)''')
        
    def process_item(self, item, spider):
        self.cur.execute('''INSERT INTO projects
                         (link, name, price, tags, time,
                         date, views, responses, description,
                         description_links, user_files)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (item['link'], item['name'], item['price'],
                          item['tags'], item['time'], item['date'],
                          item['views'], item['responses'], item['description'],
                          item['description_links'], item['user_files'],
                          ),
                         )
        self.con.commit()
        
        return item
