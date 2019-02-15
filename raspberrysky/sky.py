import math
import skyfield.api as skyfield

from skyfield.data import hipparcos

class Sky():
    def __init__(self, settings):
        loader = skyfield.Loader('skyfield-data', expire=False)
        
        self.__planets = loader('de421.bsp')
        self.__stars = hipparcos.load_dataframe(loader.open(hipparcos.URL))

        self.__site = self.__planets['earth'] + skyfield.Topos(
            latitude_degrees=settings['latitude'],
            longitude_degrees=settings['longitude'],
            elevation_m=settings['elevation']
        )
        
        self.__timescale = loader.timescale()
        
    def findStar(self, designation):
        star = skyfield.Star.from_dataframe(self.__stars.loc[designation])
        
        return self.__getAltAz(star)

    def findPlanet(self, name):
        planet = self.__planets[name]

        return self.__getAltAz(planet)

    def __getAltAz(self, object):
        altaz = self.__site.at(self.__timescale.now()).observe(object).apparent().altaz()

        return (altaz[0].degrees, altaz[1].degrees)