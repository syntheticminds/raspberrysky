import ephem
import math

class Sky():
    def __init__(self, settings):
        self.__site = ephem.Observer()

        self.__site.lon = math.radians(settings['longitude'])
        self.__site.lat = math.radians(settings['latitude'])
        self.__site.elevation = settings['elevation']

    def whereIsPolaris(self):
        polaris = ephem.star('Polaris')
        polaris.compute(self.__site)

        return (math.degrees(polaris.az), math.degrees(polaris.alt))

    def whereIsTheMoon(self):
        moon = ephem.Moon()
        moon.compute(self.__site)

        return (math.degrees(moon.az), math.degrees(moon.alt))
