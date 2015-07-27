#TODO: cada vegada que es creï nou
def hangar_kml(placemarks, filename, icon_path, style_name):
    with open(filename, "w") as kml_file:
        kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                          + "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n"
                          + "\t<Document>\n"
                          + "\t\t<Style id=\"" + style_name + "\">\n"
                          + "\t\t\t<IconStyle>\n"
                          + "\t\t\t\t<Icon>\n"
                          + "\t\t\t\t\t<href>" + icon_path + "</href>\n"
                          + "\t\t\t\t\t<scale>1.0</scale>\n"
                          + "\t\t\t\t</Icon>\n"
                          + "\t\t\t</IconStyle>\n"
                          + "\t\t</Style>\n")

        for placemark in placemarks:
            kml_file.write("\t\t<Placemark>\n"
                              + "\t\t\t<name>" + placemark.name + "</name>\n"
                              + "\t\t\t<description>" + placemark.description + "</description>\n"
                              + "\t\t\t<styleUrl>" + style_name + "</styleUrl>\n"
                              + "\t\t\t<Point>\n"
                              + "\t\t\t\t<altitudeMode>absolute</altitudeMode>\n"
                              + "\t\t\t\t<coordinates>"
                              + placemark.longitude + "," + placemark.latitude + "," + placemark.altitude
                              + "</coordinates>\n"
                              + "\t\t\t</Point>\n"
                              + "\t\t</Placemark>\n")
        kml_file.write("\t</Document>\n"
                       + "</kml>")
