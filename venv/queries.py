import mysql.connector
from mysql.connector import Error
import json

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="newrootpassword",
        database="test"
    )
    if mydb.is_connected():
        db_info = mydb.get_server_info()
        print("Connected to MySQL database... MySQL Server version on ", db_info)
        mycursor = mydb.cursor()
        mycursor.execute("")
        codes = []
        with open("data.json", encoding="utf-8") as jsonfile:
            jsonobjs = json.load(jsonfile)

        for item in jsonobjs:
            pn, pc, cn, cc, rn, rc = item["Province Name"], item["Province Code"], item['County Name'], item[
                "County Code"], item["Region Name"], item['Region ID']
            if pc not in codes:
                mycursor.execute("INSERT INTO region_all (code, name, parent_code) VALUES (%s, %s, %s);", (pc, pn, 0))
                codes.append(pc)

            if cc not in codes:
                mycursor.execute("INSERT INTO region_all (code, name, parent_code) VALUES (%s, %s, %s);", (cc, cn, pc))
                codes.append(cc)

            if rc not in codes:
                mycursor.execute("INSERT INTO region_all (code, name, parent_code) VALUES (%s, %s, %s);", (rc, rn, cc))
                codes.append(rc)

except Error as e:
    print("Error", e.args)

finally:
    if (mydb.is_connected()):
        mydb.commit()
        mycursor.close()
        mydb.close()
        print("Connection Closed")
