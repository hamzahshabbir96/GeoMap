#helper Functiondef
from django.contrib.gis.geoip2 import GeoIP2
def get_geo(ip):
    g=GeoIP2()
    country=g.country(ip)
    city=g.city(ip)
    lat,lon=g.lat_lon(ip)
    return country,city,lat,lon

def middle_Coord(lattA,lonnA,lattB=None,lonnB=None):
    cord=(lattA,lonnA)
    if lattB:
        cord=[(lattA+lattB)/2,(lonnA+lonnB)/2]
    return cord

def zoom_scale(distance):
    if distance <= 50:
        return 9
    elif distance<50 and distance<=100:
        return 8
    elif distance> 100 and distance<= 4000:
        return 4
    else:
        return 2
