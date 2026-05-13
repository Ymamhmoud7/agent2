import geocoder
from geopy.geocoders import Nominatim

def get_current_location():
    g = geocoder.ip('me')
    latlng = g.latlng
    if latlng is None:
        return "Unable to determine location"
    lat, long = g.latlng

    geoLoc = Nominatim(user_agent="GetLoc")
    locName = geoLoc.reverse(f"{lat}, {long}")
    return locName.address
