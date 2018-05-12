'''
GooMPy: Google Maps for Python

Copyright (C) 2015 Alec Singer and Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.
This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.

@edit: Sandra Moen, https://github.com/Slideshow776, winter/spring 2018
    Implemented:
        - Multithreading, grabbing tiles is now ~4x faster.
        - Dragging the mouse using the method 'move' changes latitude and longitude coordinates.
        - Fixed a bug where maptype would give a completely different view.
        - Api key is now fetched from api_key.txt, which should be manually made containing a google static map api key.
        - Now support map coordinates as a list of lists: [[lat_a,_lon_a, size_a, #color_a],[lat_b,lon_b, size_b, #color_b],...[lat_z,lon_z, size_z, #color_z]]
        - Mousewheel zooming using the method 'move and zoom'.
'''

import math, sys, os, time, threading
import PIL.Image

from io import BytesIO

import urllib.request
import polyline
urlopen = urllib.request.urlopen

try:
    FILE = open("api_key.txt", "r") # Loading keys from hidden textfile, in order to protect private keys from misuse
    _KEY = FILE.readlines()[0]
    if not _KEY: print("Error: could not read api key from api_key.txt")
except: 
    print("Error: could not open api_keys.txt")

_EARTHPIX = 268435456  # Number of pixels in half the earth's circumference at zoom = 21
_DEGREE_PRECISION = 4  # Number of decimal places for rounding coordinates
_TILESIZE = 640        # Larget tile we can grab without paying
_GRABRATE = 4          # Fastest rate at which we can download tiles without paying
_pixrad = _EARTHPIX / math.pi
 
def _new_image(width, height): return PIL.Image.new('RGB', (width, height))
def _roundto(value, digits): return int(value * 10**digits) / 10.**digits
def _pixels_to_degrees(pixels, zoom): return pixels * 2 ** (21 - zoom)

def _grab_tile(lat, lon, zoom, maptype, coordinates, _TILESIZE, sleeptime): # This method was edited by Sandra Moen
    urlbase = (
        "https://maps.googleapis.com/maps/api/staticmap?"
        "center=%f,%f"
        "&zoom=%d"
        "&maptype=%s"
        "&size=%dx%d"
        "&format=jpg"
        )    
    specs = lat, lon, zoom, maptype, _TILESIZE, _TILESIZE
    #filename = 'mapscache/' + ('%f_%f_%d_%s_%d_%d' % specs) + '.jpg'

    #if os.path.isfile(filename):
        #tile = PIL.Image.open(filename)
    #else:
    url = urlbase % specs
    for i in range(len(coordinates[0])):
        # TODO: apply color based on c[2]'s variance variable, 'c92240' is the color part ...
        url += "&path=fillcolor:0x" + coordinates[1][i] + "bb%7Cweight:1%7Ccolor:0x000000ff%7Cenc:"+coordinates[0][i]
    url += "&key=" + _KEY
    #print("Requesting image from google, URL: ", url)
    result = urlopen(url).read()
    #print("Google result: ", result)
    tile = PIL.Image.open(BytesIO(result))
    #if not os.path.exists('mapscache'): os.mkdir('mapscache')
    #tile.save(filename)
    #time.sleep(sleeptime) # Choke back speed to avoid maxing out limit
    return tile

def _pix_to_lon(j, lonpix, ntiles, _TILESIZE, zoom):
    return math.degrees((lonpix + _pixels_to_degrees(((j)-ntiles/2)*_TILESIZE, zoom) - _EARTHPIX) / _pixrad)

def _pix_to_lat(k, latpix, ntiles, _TILESIZE, zoom):
    return math.degrees(math.pi/2 - 2 * math.atan(math.exp(((latpix + _pixels_to_degrees((k-ntiles/2)*_TILESIZE, zoom)) - _EARTHPIX) / _pixrad))) 

def fetchTiles(latitude, longitude, zoom, maptype, coordinates, radius_meters=None, default_ntiles=4):
    '''
    Fetches tiles from GoogleMaps at the specified coordinates, zoom level (0-22), and map type ('roadmap', 
    'terrain', 'satellite', or 'hybrid').  The value of radius_meters deteremines the number of tiles that will be 
    fetched; if it is unspecified, the number defaults to default_ntiles.  Tiles are stored as JPEG images 
    in the mapscache folder.
    '''    

    latitude = _roundto(latitude, _DEGREE_PRECISION)
    longitude = _roundto(longitude, _DEGREE_PRECISION)

    # https://groups.google.com/forum/#!topic/google-maps-js-api-v3/hDRO4oHVSeM
    pixels_per_meter = 2**zoom / (156543.03392 * math.cos(math.radians(latitude)))

    # number of tiles required to go from center latitude to desired radius in meters
    ntiles = default_ntiles if radius_meters is None else int(round(2 * pixels_per_meter / (_TILESIZE /2./ radius_meters))) 
    
    lonpix = _EARTHPIX + longitude * math.radians(_pixrad)

    sinlat = math.sin(math.radians(latitude))
    latpix = _EARTHPIX - _pixrad * math.log((1 + sinlat)/(1 - sinlat)) / 2

    bigsize = ntiles * _TILESIZE
    bigimage = _new_image(bigsize, bigsize)

    def _thread_get_tile_and_put_in_bigimage(k, latpix, ntiles, _TILESIZE, zoom, lon, maptype, coordinates, _GRABRATE, j):
        lat = _pix_to_lat(k, latpix, ntiles, _TILESIZE, zoom)
        tile = _grab_tile(lat, lon, zoom, maptype, coordinates, _TILESIZE, 1./_GRABRATE)
        bigimage.paste(tile, (j*_TILESIZE,k*_TILESIZE))

    threads = []
    for j in range(ntiles):
        lon = _pix_to_lon(j, lonpix, ntiles, _TILESIZE, zoom)
        for k in range(ntiles):
            t = threading.Thread(
                target=_thread_get_tile_and_put_in_bigimage,
                args=(k, latpix, ntiles, _TILESIZE, zoom, lon, maptype, coordinates, _GRABRATE, j,))
            threads.append(t)
            t.start()

    west = _pix_to_lon(0, lonpix, ntiles, _TILESIZE, zoom)
    east = _pix_to_lon(ntiles-1, lonpix, ntiles, _TILESIZE, zoom)

    north = _pix_to_lat(0, latpix, ntiles, _TILESIZE, zoom)
    south = _pix_to_lat(ntiles-1, latpix, ntiles, _TILESIZE, zoom)

    for t in threads: # wait untill all threads have finished
        t.join()

    return bigimage, (north,west), (south,east)

class GooMPy(object):
    def __init__(self, width, height, latitude, longitude, zoom,
         maptype, coordinates, radius_meters=None, default_ntiles=4):
        '''
        Creates a GooMPy object for specified display widthan and height at the specified coordinates,
        zoom level (0-22), and map type ('roadmap', 'terrain', 'satellite', or 'hybrid').
        The value of radius_meters deteremines the number of tiles that will be used to create
        the map image; if it is unspecified, the number defaults to default_ntiles.  
        '''
        self.lat = latitude
        self.lon = longitude

        self.width = width
        self.height = height

        self.zoom = zoom
        self.maptype = maptype
        self.radius_meters = radius_meters
        self.coordinates = coordinates

        self.winimage = _new_image(self.width, self.height)

        self._fetch()

        halfsize = int(self.bigimage.size[0] / 2)
        self.leftx = halfsize
        self.uppery = halfsize

        self._update()

    def _drawCircle(self, coordinates, zoom, radius=.0003): # Low polygon circle (it's a diamond)
        encodedCircledCoordinates = []
        color_coordinates = []
        radius = radius * (1/zoom*zoom)
        for c in coordinates:
            radius += c[2]
            n = (c[0] + radius, c[1])
            w = (c[0], c[1] - radius*2) # west and east coordinates needs to be doubled(?)
            s = (c[0] - radius, c[1])
            e = (c[0], c[1] + radius*2) # west and east coordinates needs to be doubled(?)
            radius -= c[2]
            encodedCircledCoordinates.append(polyline.encode([n, w, s, e, n])) # the extra n closes the loop drawn
            color_coordinates.append(c[3])
        return [encodedCircledCoordinates, color_coordinates]

    def getImage(self): return self.winimage # Returns the current image as a PIL.Image object.
    def getCoordinates(self): return self.coordinates
    
    def _set_lat_lon_with_deltas(self, dx, dy):
        w, h = _TILESIZE, _TILESIZE
        zoom = self.zoom
        lat = self.lat
        lng = self.lon
        x, y = (w/2) + dx, (h/2) + dy

        degreesPerPixelX = 360 / math.pow(2, zoom + 8)
        degreesPerPixelY = 360 / math.pow(2, zoom + 8) * math.cos(lat * math.pi / 180)

        self.lat = lat + degreesPerPixelY * ( y - w / 2)
        self.lon = lng + degreesPerPixelX * ( x  - w / 2)
        #print('lat, lon: ', self.lat, self.lon)

    def move(self, dx, dy):
        '''
        Moves the view by the specified pixels dx, dy.
        '''
        self._set_lat_lon_with_deltas(dx, dy*-1)
                
        self.leftx = self._constrain(self.leftx, dx, self.width)
        self.uppery = self._constrain(self.uppery, dy, self.height)
        self._update()
        #print("Moved: " + str(self.lat) + ", " + str(self.lon))

    def move_and_zoom(self, prex, prey, zoom):
        w, h = _TILESIZE, _TILESIZE
        dx = prex - (w/2) # lon, lat is origo, this ensures correct quadrant of deltas
        dy = (h/2) - prey

        self._set_lat_lon_with_deltas(dx, dy)   

        self.leftx = self._constrain(self.leftx, dx, self.width)
        self.uppery = self._constrain(self.uppery, dy, self.height)
        
        self.useZoom(zoom)

    def useMaptype(self, maptype):
        '''
        Uses the specified map type 'roadmap', 'terrain', 'satellite', or 'hybrid'.
        Map tiles are fetched as needed.
        '''
                
        self.maptype = maptype
        self._fetch()
        halfsize = int(self.bigimage.size[0] / 2)
        self.leftx = halfsize
        self.uppery = halfsize
        self._update()

    def useZoom(self, zoom):
        '''
        Uses the specified zoom level 0 through 22.
        Map tiles are fetched as needed.
        '''
        
        self.zoom = zoom
        self._fetch()
        halfsize = int(self.bigimage.size[0] / 2)
        self.leftx = halfsize
        self.uppery = halfsize
        self._update()

    def _fetch_and_update(self):
        self._fetch()
        self._update()

    def _fetch(self):
        self.bigimage, self.northwest, self.southeast = fetchTiles(
            self.lat,
            self.lon,
            self.zoom,
            self.maptype,
            self._drawCircle(self.coordinates, self.zoom),
            self.radius_meters
        )

    def _update(self): 
        self.winimage.paste(self.bigimage, (-int(self.leftx), -int(self.uppery)))

    def _constrain(self, oldval, diff, dimsize):
        newval = oldval + diff
        return newval if newval > 0 and newval < self.bigimage.size[0]-dimsize else oldval
