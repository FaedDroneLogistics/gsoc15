package geoJava;/*
 * Author: Julio Bondia, Marc Gonzàlez
 * E-mail: {julio.bondia13, marcgc21}@gmail.com
 * 
 * FAED Project - Google Summer of Code 2015
 */

import geoprojection.Circle;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;



public class KMLCircle {

	/**
	 * Generate a KML file of a circle with center (centerLat, centerLon) of radius 'radius'
	 * 
	 * @param circle - circle to draw
	 * @throws java.io.IOException
	 */
	public static List<String> genCircle(Circle circle) throws IOException {
		
		String zoneAndLetter;
		double utmX, utmY;
		double utmCenterX, utmCenterY;
			
		String utmStr;
		String[] latLonStr;
		double[] projectedPoint;
		GeoTool geoTool = new GeoTool();

		List<String> circlePoints = new ArrayList<String>();
			
		utmStr = geoTool.latLon2UTM(circle.getLat(), circle.getLon());
		latLonStr = utmStr.split("\\s+");

		zoneAndLetter = latLonStr[0] + " " + latLonStr[1];
		utmCenterX = Double.parseDouble(latLonStr[2]);
		utmCenterY = Double.parseDouble(latLonStr[3]);
	
		for(int i = 0; i <= 360; i++) {

			utmX = circle.getRadius() * Math.cos(Math.toRadians(i)) + utmCenterX;
			utmY = circle.getRadius() * Math.sin(Math.toRadians(i)) + utmCenterY;

			projectedPoint = geoTool.utm2LatLon(zoneAndLetter + " " + utmX + " " + utmY);
			circlePoints.add(projectedPoint[1] + "," + projectedPoint[0] + "," + circle.getAltitude());
		}

		return circlePoints;
	}
}
