# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import time

class ScrapyAppPipeline:
    def process_item(self, item, spider):
        return item

class PostgresPipeline:
    def open_spider(self, spider):
        # Use the Docker service name `postgres` as the hostname
        hostname = 'postgres'  # Docker service name for PostgreSQL
        username = 'youruser'  # Your PostgreSQL user
        password = 'yourpassword'  # Your PostgreSQL password
        database = 'yourdbname'  # Your PostgreSQL database
        port=5432
        retries = 20  # Number of retries
        delay = 2  # Delay in seconds between retries
        for attempt in range(retries):
            try:
                self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
                self.cur = self.connection.cursor()
                print("Database connected")
                # Truncate the estate_items table at the start of the spider
                self.cur.execute("TRUNCATE TABLE estate_items RESTART IDENTITY")
                self.connection.commit()
                print("Cleared all data from estate_items.")
                break  # Successful connection, break out of the loop
            except psycopg2.OperationalError as e:
                if attempt < retries - 1:
                    wait = delay * (2 ** attempt)  # Exponential backoff
                    spider.logger.error(f"Database connection failed, retrying in {wait} seconds...")
                    time.sleep(wait)
                else:
                    spider.logger.error("Maximum retries reached, could not connect to the database.")
                    raise e

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        # Insert data into the `estate_items` table
        self.cur.execute("INSERT INTO estate_items(title, image_url) VALUES(%s, %s)", (item['title'], item['first_image_url']))
        self.connection.commit()
        return item