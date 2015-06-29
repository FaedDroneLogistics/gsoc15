from django.db import models

class StyleURL(models.Model):
    href = models.URLField()
    scale = models.FloatField()

    def __unicode__(self):
        return str(self.href)

class DropPoint(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    is_available = models.BooleanField(default=True)
    style_url = models.ForeignKey(StyleURL)

    def __unicode__(self):
        return str(self.name)

class Drone(models.Model):
    plate = models.CharField(max_length=50)
    origin_lat = models.FloatField()
    origin_lon = models.FloatField()
    destination_lat = models.FloatField()
    destination_lon = models.FloatField()

    def __unicode__(self):
        return str(self.plate)

class Hangar(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    radius = models.FloatField()
    is_available = models.BooleanField(default=True)
    style_url = models.ForeignKey(StyleURL)
    drop_points = models.ManyToManyField(DropPoint)
    drone = models.ForeignKey(Drone)

    def __unicode__(self):
        return str(self.name)

class MeteoStation(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    is_available = models.BooleanField(default=True)
    style_url = models.ForeignKey(StyleURL)
    temperature = models.FloatField()
    wind_speed = models.FloatField()



#class Point(models.Model):
#    name = models.CharField(max_length=50)
#    description = models.TextField()
#    latitude = models.FloatField()
#    longitude = models.FloatField()
#    altitude = models.FloatField()
#    style_url = models.ForeignKey(StyleURL)
#
#    def __unicode__(self):
#        return str(self.name)
#
#class DropPoint(models.Model):
#    point = models.ForeignKey(Point)
#    is_available = models.BooleanField(default=True)
#
#class Drone(models.Model):
#    origin = models.ForeignKey(Point, related_name="drone_origin")
#    destination = models.ForeignKey(Point, related_name="drone_destination")
#
#class Hangar(models.Model):
#    #name = models.CharField(max_length=2,blank=True)
#    point = models.ForeignKey(Point)
#    radius = models.FloatField()
#    is_available = models.BooleanField(default=True)
#    drop_points = models.ManyToManyField(DropPoint)
#    drone = models.ForeignKey(Drone)
#
#    def __unicode__(self):
#        return str(self.point.name)
#
#class Emergency(models.Model):
#    point = models.ForeignKey(Point)
#
#class Station(models.Model):
#    point = models.ForeignKey(Point)
#    is_available = models.BooleanField()
