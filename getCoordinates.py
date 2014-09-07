import urllib, json
import mysql.connector
import time
import urlparse


#response = urllib.urlopen(url);
#data = json.loads(response.read())


cnx = mysql.connector.connect(user='pedro', password='',
                              host='127.0.0.1',
                              database='pymeclick_base')

cursor = cnx.cursor(buffered=True)


query = ("Select nombre_municipio from municipios WHERE latitud IS NULL")

rs = cursor.execute(query)
rs = cursor.fetchall()





for (nombre_estado) in rs:

    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true_or_false&region=mx"  %nombre_estado
    n = "%s" %nombre_estado
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
    
        add_latLong = ("UPDATE municipios SET latitud=%s, longitud=%s WHERE nombre_municipio=\'%s\';" %(latitud, longitud, n))
        print (add_latLong)
        cursor.execute(add_latLong)
        cnx.commit()
    if(data["status"] == "OVER_QUERY_LIMIT"):
        print n
        print data["status"]
        time.sleep(2)

    else:
        print n
        print data["status"]



cursor.close()
cnx.commit()
cnx.close()
