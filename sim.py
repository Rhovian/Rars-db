import time
import random
import psycopg2
from psycopg2 import pool, extras
from contextlib import contextmanager

class Node():
    def __init__(self):
        self.conn = psycopg2.pool.SimpleConnectionPool(
            1,
            10,
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost", # postgres ~ docker config | 127.0.0.1 ~ local config
            port="5432",
        )
        self.film = 'TEST_FILM_SOCKET'
        self.box = 'TEST_BOX_SOCKET'
        self.storage_cabinet = 'TEST_CABINET'

    @contextmanager
    def db(self):
        con = self.conn.getconn()
        cur = con.cursor()
        try:
            yield con, cur
        finally:
            cur.close()
            self.conn.putconn(con)

    def update_film(self, type):
        # data: film ID, box ID, cabinet ID, Location (staging), timestamp
        # type: staged, boxed, stored\
        with self.db() as (connection, cursor):
            try:
                if type == 'staged':
                    query = "UPDATE films set location = %s, ts = %s where film_id = %s"
                    cursor.execute(query, ('staging', time.time(), self.film))    # If the film is not in a box, it is in the staging area. 
                    print('Simulation: film in staging area...')              # It has either not been stored or has been retrieved.
                
                elif type == 'boxed':
                    query = "UPDATE films set location = %s, box_id = %s, ts = %s where film_id = %s" # TODO: Define location type for real system.
                    # Box holds 100 slides, this next function generates a random location
                    location = self.gen_loc(self.box)
                    cursor.execute(query, (location, self.box, time.time(), self.film))
                    print('Simulation: film in box: {} | location: {} ...'.format(self.box, self.film))

                else:
                    print('Update: {} | Wrong type').format(type)

                connection.commit()

            except Exception as e:
                print(e)

    def update_box(self, stored):
        # data: Box ID, cabinet ID, timestamp
        # type: stored (T/F)
        with self.db() as (connection, cursor):
            try:
                if stored:
                    query = "UPDATE boxes set cabinet_id = %s, ts = %s where box_id = %s"
                    location = self.gen_loc(self.storage_cabinet)
                    cursor.execute(query, (location, time.time(), self.box))    # If the film is not in a box, it is in the staging area. 
                    print('Simulation: box has been stored: {}'.format(location))
                
                elif not stored:
                    query = "UPDATE boxes set cabinet_id = %s, ts =%s where box_id = %s"
                    cursor.execute(query, (None, time.time(), self.box))
                    print('Simulation: box is not in the storage cabinet anymore ...')

                connection.commit()

            except Exception as e:
                print(e) 

    def gen_loc(self, base):
        return base + '_' + str(random.randint(1,101))

    def store_film(self):
        self.update_film('staged')
        # film stored in box
        self.update_film('boxed')
        # box storage
        self.update_box(True)

    def retrieve_film(self):
        self.update_film('staged')
        self.update_box(False)


    def run(self):

        while True:
        # instantiates film journey thread
        # staging -> box stored -> cabinet stored
            self.store_film()
            time.sleep(3)
            self.retrieve_film()
            
            time.sleep(10)
        
        # staging <- box stored <- cabinet stored
        pass


if __name__ == '__main__':
    db = Node()
    db.run()