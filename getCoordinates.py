import urllib, json
import MySQLdb
import time
import urlparse
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="root", # your password
                      db="estados") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

query = ("select e.nombre, m.nombre, m.id from estados e, municipios m WHERE e.id = m.estado_id AND m.latitud is NULL;")


# Use all the SQL you like
cur.execute(query)

# print all the first cell of all the rows
for row in cur.fetchall() :
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s,%s&sensor=true_or_false&region=mx"  %(row[0], row[1])
    url = unicode(url, errors='ignore')
    url = url.encode('utf8')
    response = urllib.urlopen(url);
    data = json.loads(response.read())
    
    
    if(data["status"] == "OK"):
        #print json.dumps(data, indent=4, sort_keys=True)
        print url
        print data["status"]

        latitud = data["results"][0]["geometry"]["location"]["lat"]
        longitud =data["results"][0]["geometry"]["location"]["lng"]
    
        time.sleep(.1)
    
        add_latLong = ("UPDATE municipios SET latitud=%s, longitud=%s WHERE id=\'%s\';" %(latitud, longitud, row[2]))
        print (add_latLong)
        cur.execute(add_latLong)

    

    if(data["status"] == "OVER_QUERY_LIMIT"):
        print row[1]
        print data["status"]
        time.sleep(2)

    else:
        print row[1]
        print data["status"]


