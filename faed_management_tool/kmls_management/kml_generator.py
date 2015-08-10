import random

def placemark_kml(placemark, filename):
    with open(filename, "w") as kml_file:
        kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                       + "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n"
                       + "\t<Document>\n"
                       + "\t\t<Style id=\"" + placemark.style_url.name.lower().replace(" ", "_") + "\">\n"
                       + "\t\t\t<IconStyle>\n"
                       + "\t\t\t\t<Icon>\n"
                       + "\t\t\t\t\t<href>" + placemark.style_url.href + "</href>\n"
                       + "\t\t\t\t\t<scale>1.0</scale>\n"
                       + "\t\t\t\t</Icon>\n"
                       + "\t\t\t</IconStyle>\n"
                       + "\t\t</Style>\n"
                       + "\t\t<Placemark>\n"
                       + "\t\t\t<name>" + placemark.name + "</name>\n"
                       + "\t\t\t<description>" + placemark.description + "</description>\n"
                       + "\t\t\t<styleUrl>" + placemark.style_url.name.lower().replace(" ", "_") + "</styleUrl>\n"
                       + "\t\t\t<Point>\n"
                       + "\t\t\t\t<altitudeMode>relativeToGround</altitudeMode>\n"
                       + "\t\t\t\t<coordinates>"
                       + str(placemark.longitude) + "," + str(placemark.latitude) + "," + str(placemark.altitude)
                       + "</coordinates>\n"
                       + "\t\t\t</Point>\n"
                       + "\t\t</Placemark>\n"
                       + "\t</Document>\n"
                       + "</kml>")


def circle_kml(points, filename):
    with open(filename, "w") as kml_file:
        kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                       + "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n"
                       + "\t<Document>\n"
                       + "\t\t<name>Influence Radius</name>\n"
                       + "\t\t<visibility>1</visibility>\n"
                       + "\t\t<Placemark>\n"
                       + "\t\t\t<name>Hangar</name>\n"
                       + "\t\t\t<visibility>1</visibility>\n"
                       + "\t\t\t<Style>\n"
                       + "\t\t\t\t<LineStyle>\n"
                       + "\t\t\t\t\t<color>" + random_color() + "</color>\n"
                       + "\t\t\t\t\t<scale>1</scale>\n"
                       + "\t\t\t\t\t<width>10</width>\n"
                       + "\t\t\t\t</LineStyle>\n"
                       + "\t\t\t</Style>\n"
                       + "\t\t\t<LineString>\n"
                       + "\t\t\t\t<altitudeMode>absolute</altitudeMode>\n"
                       + "\t\t\t\t<coordinates>\n")
        for p in points:
            kml_file.write("\t\t\t\t" + p + "\n")

        kml_file.write("\t\t\t\t</coordinates>\n"
                       + "\t\t\t</LineString>\n"
                       + "\t\t</Placemark>\n"
                       + "\t</Document>\n"
                       + "</kml>")

def random_color():
    r = lambda: random.randint(0,255)
    return '%02X%02X%02X%02X' % (r(),r(),r(),r())