#! /usr/bin/python3

from datetime import datetime
import sqlite3
import os

class TempDB:
    def __init__(self):

        self.location = 'data'
        self.file = "x2temp.txt"
        self.database = "x2cfmap.db"
        self.con = sqlite3.connect(f"{self.location}/{self.database}")
        self.cursor = self.con.cursor()
        self.file_list = []
        self.file_dict = {}
        self.db_dict = {}
        self.increment_a = 0
        self.increment_b = 7
        self.to_fahr = lambda temp: float("{:.2f}".format((float(temp) * 9/5) + 32))

    def from_file(self):
        with open(self.location + "/" + self.file) as f:
            self.xfile = f.read()
        f.close()

    def file_data(self):
        # Convert datetime
        self.new_list = self.xfile.split()[3:]

        for increment in range(int(len(self.new_list) / 7)):

            self.entry = self.new_list[self.increment_a:self.increment_b]
            self.entry = [self.entry[0], ' '.join(self.entry[1:])]

            self.increment_a += 7
            self.increment_b += 7

            self.unformatted_celsius = self.entry[0]
            self.unformatted_datetime = self.entry[1]

            self.celsius = self.unformatted_celsius.strip("temp=").strip("'C")
            if '\x00' in self.celsius:
                continue
            self.fahr = self.to_fahr(self.celsius)
            self.datetime = datetime.strptime(self.unformatted_datetime, '%a %b %d %H:%M:%S %Z %Y')

            self.dt_date, self.dt_time = str(self.datetime).split()
            self.db_dt = self.dt_date + ' ' + self.dt_time

            self.file_dict[increment+1] = [self.celsius, self.fahr, self.db_dt]

    def to_database(self):

        keys = list(self.file_dict)
        idx = 0
        
        self.cursor.execute("""
            SELECT seq FROM sqlite_sequence
        """)
        seq = self.cursor.fetchall()

        if seq == []:
            pass
        else:
            seq = seq[0][0]
            idx = keys.index(seq)
            keys = keys[idx+1:]


        for data in keys:
            ROWID = data
            cels, fahr = self.file_dict[data][:2]
            dt = self.file_dict[data][2]
            self.cursor.execute(f"""INSERT INTO temperature ('ROWID','celsius','fahrenheit','datetime')
            values ({ROWID}, {cels}, {fahr}, '{dt}')""")

        self.con.commit()


tdb = TempDB()
tdb.from_file()
tdb.file_data()
tdb.to_database()
