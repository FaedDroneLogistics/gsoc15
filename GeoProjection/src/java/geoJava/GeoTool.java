package geoJava;/*
 * Author: Sami Salkosuo
 * E-mail: sami.salkosuo@fi.ibm.com
 * (c) Copyright IBM Corp. 2007
 * Terms of use: http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=250050&filename=j-coordconvert.zip&method=http&locale=
 * 
 * Modified by: Julio Bondia, Marc Gonzàlez
 * E-mail: {julio.bondia13, marcgc21}@gmail.com
 * 
 * FAED Project - Google Summer of Code 2015
 */

public class GeoTool {
	
	private final static int EARTH_STANDARD_RADIUS = 6378100; //In meters

	/**
	 * Convert from UTM format to latitude, longitude 
	 * 
	 * @param UTM - Concatenated String containing the UTM position
	 * @return [latitude, longitude]
	 */
	public double[] utm2LatLon(String UTM) {
		
		UTM2LatLon c = new UTM2LatLon();
		return c.convertUTMToLatLong(UTM);
	}

	/**
	 * Convert from latitude, longitude format to UTM
	 * 
	 * @param latitude - latitude coordinate
	 * @param longitude - longitude coordinate
	 * @return String containing the UTM format from the given position
	 */
	public String latLon2UTM(double latitude, double longitude) {
		
	    LatLon2UTM c = new LatLon2UTM();
	    return c.convertLatLonToUTM(latitude, longitude);
	}

	/**
	 * Validate correct format of the parameters
	 * 
	 * @param latitude - latitude coordinate
	 * @param longitude - longitude coordinate
	 */
	private void validate(double latitude, double longitude) {
		
		if (latitude < -90.0 || latitude > 90.0 || longitude < -180.0
				|| longitude >= 180.0) {
			throw new IllegalArgumentException("Legal ranges: latitude [-90,90]"
					+ ", longitude [-180,180).");
		}
	}
	
	/**
	 * Calculate if a point is inside a circle with center centerLat, centerLong and radius 'radius'
	 * 
	 * @param centerLat
	 * @param centerLon
	 * @param lat
	 * @param lon
	 * @param radius
	 * @return true if it is in the circle, false otherwise
	 * @throws NotTheSameZoneException
	 */
	public boolean isInCircle(double centerLat, double centerLon, double lat, double lon, double radius) {
		
		return distance(centerLat, centerLon, lat, lon)[0] <= radius;		
	}
	
	/**
	 * Calculate the distance between two points, whatever their zone is.
	 * 
	 * @param centerLat - origin latitude
	 * @param centerLon - origin longitude
	 * @param lat - destiny latitude
	 * @param lon - destiny longitude
	 * @return [distance (in meters), angle (in degrees)]
	 */
	public double[] distance(double centerLat, double centerLon, double lat, double lon) {
		
		double[] distanceAngle = new double[2];
		double latRad = Math.toRadians(lat);
		double lonRad = Math.toRadians(lon);
		double centerLatRad = Math.toRadians(centerLat);
		double centerLonRad = Math.toRadians(centerLon);
		
		//Calculate distance in meters
		distanceAngle[0] = Math.acos(Math.sin(centerLatRad) * Math.sin(latRad)
				+ Math.cos(centerLatRad) * Math.cos(latRad) * Math.cos(lonRad - centerLonRad))
				* EARTH_STANDARD_RADIUS;
		
		//Calculate angle in degrees
		double y = Math.sin(lonRad - centerLonRad) * Math.cos(latRad);
		double x = Math.cos(centerLatRad) * Math.sin(latRad) -
		        Math.sin(centerLatRad) * Math.cos(latRad) * Math.cos(lonRad - centerLonRad);
		double bearing = Math.atan2(y, x);
		
		distanceAngle[1] = (Math.toDegrees(bearing) + 360) % 360; // Bearing to degrees and normalize to 0..360º
		
		//System.out.println("Distance => " + distanceAngle[0] + "\nAngle => " + distanceAngle[1]);
		
		return distanceAngle;
	}
	
	
	/*** LatLon2UTM ***/
	
	private class LatLon2UTM {
		
		// Lat Lon to UTM variables	
	    // equatorial radius
	    double equatorialRadius = 6378137;
	
	    // polar radius
	    double polarRadius = 6356752.314;
	
	    // scale factor
	    double k0 = 0.9996;
	
	    // eccentricity
	    double e = Math.sqrt(1 - Math.pow(polarRadius / equatorialRadius, 2));	
	    double e1sq = e * e / (1 - e * e);
	
	    // r curv 2
	    double nu = 6389236.914;
	
	    // Calculate Meridional Arc Length
	    // Meridional Arc
	    double S = 5103266.421;	
	    double A0 = 6367449.146;	
	    double B0 = 16038.42955;	
	    double C0 = 16.83261333;	
	    double D0 = 0.021984404;	
	    double E0 = 0.000312705;
	
	    // Calculation Constants
	    // Delta Long
	    double p = -0.483084;	
	    double sin1 = 4.84814E-06;
	
	    // Coefficients for UTM Coordinates
	    double K1 = 5101225.115;	
	    double K2 = 3750.291596;	
	    double K3 = 1.397608151;	
	    double K4 = 214839.3105;	
	    double K5 = -2.995382942;
		
	    /**
		 * Procedures to onvert from latitude, longitude format to UTM
		 * 
		 * @param latitude - latitude coordinate
		 * @param longitude - longitude coordinate
		 * @return String containing the UTM format from the given position
		 */
		public String convertLatLonToUTM(double latitude, double longitude) {

			validate(latitude, longitude);
			String UTM = "";
	
			setVariables(latitude, longitude);
	
			//String longZone = getLongZone(longitude);
			LatZones latZones = new LatZones();
			String latZone = latZones.getLatZoneLetter(latitude, longitude);
	
			double easting = getEasting();
			double northing = getNorthing(latitude);
	
			UTM = latZone + " " + easting + " " + northing;
			
			return UTM;	
	    }
	
		/**
		 * Initialize the needed variables to convert latitude, longitude to UTM
		 * 
		 * @param latitude - latitude coordinate
		 * @param longitude - longitude coordinate
		 */
	    protected void setVariables(double latitude, double longitude) {
	    	
	    	latitude = Math.toRadians(latitude);
	    	nu = equatorialRadius / Math.pow(1 - Math.pow(e * Math.sin(latitude), 2), (1 / 2.0));
	
	    	double var1;
	    	if (longitude < 0.0) {
	    		var1 = ((int) ((180 + longitude) / 6.0)) + 1;
	    	} else {
	    		var1 = ((int) (longitude / 6)) + 31;
	    	}
	    	
	    	double var2 = (6 * var1) - 183;
	    	double var3 = longitude - var2;
	    	
	    	p = var3 * 3600 / 10000;
	
	    	S = A0 * latitude - B0 * Math.sin(2 * latitude) + C0 * Math.sin(4 * latitude) - D0
	    			* Math.sin(6 * latitude) + E0 * Math.sin(8 * latitude);
	
	    	K1 = S * k0;
	    	K2 = nu * Math.sin(latitude) * Math.cos(latitude) * Math.pow(sin1, 2) * k0 * (100000000)
	    			/ 2;
	    	K3 = ((Math.pow(sin1, 4) * nu * Math.sin(latitude) * Math.pow(Math.cos(latitude), 3)) / 24)
	    			* (5 - Math.pow(Math.tan(latitude), 2) + 9 * e1sq * Math.pow(Math.cos(latitude), 2) + 4
	    			* Math.pow(e1sq, 2) * Math.pow(Math.cos(latitude), 4))	* k0 * (10000000000000000L);
	
	    	K4 = nu * Math.cos(latitude) * sin1 * k0 * 10000;
	
	    	K5 = Math.pow(sin1 * Math.cos(latitude), 3) * (nu / 6) * (1 - Math.pow(Math.tan(latitude), 2) + e1sq 
	    			* Math.pow(Math.cos(latitude), 2)) * k0 * 1000000000000L;	
	    }
	
	    /**
	     * Convert latitude to UTM northing
	     * 
	     * @param latitude - latitude coordinate
	     * @return UTM northing coordinate
	     */
	    protected double getNorthing(double latitude) {
	    	
	    	double northing = K1 + K2 * p * p + K3 * Math.pow(p, 4);
	    	
	    	if (latitude < 0.0) {
	    		northing = 10000000 + northing;
	    	}
	    	
	    	return northing;
	    }
	
	    /**
	     * Get UTM easting
	     * 
	     * @return UTM easting coordinate
	     */
	    protected double getEasting() {
	    	return 500000 + (K4 * p + K5 * Math.pow(p, 3));
	    }	
	}
	
	
	/*** UTM2LatLon ***/
	
	private class UTM2LatLon {
		
		int zone;
		double easting;	
	    double northing;	
	    String southernHemisphere = "ACDEFGHJKLM";
	    
	    double arc;	
	    double mu;	
	    double ei;	
	    double ca;	
	    double cb;	
	    double cc;	
	    double cd;	
	    double n0;	
	    double r0;	
	    double _a1;
	    double dd0;	
	    double t0;	
	    double Q0;	
	    double lof1;	
	    double lof2;	
	    double lof3;	
	    double _a2;	
	    double phi1;	
	    double fact1;	
	    double fact2;	
	    double fact3;	
	    double fact4;	
	    double zoneCM;	
	    double _a3;	
	    double a = 6378137;	
	    double e = 0.081819191;	
	    double e1sq = 0.006739497;	
	    double k0 = 0.9996;	
	
	    /**
	     * Get the hemisphere where the given zone belongs to
	     * 
	     * @param latZone 
	     * @return "N" if north hemisphere, "S" if south hemisphere
	     */
	    protected String getHemisphere(String latZone) {
	    	String hemisphere = "N";
	      
	    	if (southernHemisphere.indexOf(latZone) > -1) {
	    		hemisphere = "S";
	    	}

	    	return hemisphere;
	    }
	
	    /**
	     * Convert UTM coordinates to latitude, longitude
	     * 
	     * @param UTM - String containing the UTM format from the given position
	     * @return [latitude, longitude]
	     */
	    public double[] convertUTMToLatLong(String UTM) {
	    	
	    	double[] latlon = { 0.0, 0.0 };
	    	String[] utm = UTM.split("\\s+");

	    	zone = Integer.parseInt(utm[0]);
	    	String latZone = utm[1];
	    	easting = Double.parseDouble(utm[2]);
	    	northing = Double.parseDouble(utm[3]);
	    	String hemisphere = getHemisphere(latZone);
	    	double latitude = 0.0;
	    	double longitude = 0.0;
	
	    	if (hemisphere.equals("S")) {
	    		northing = 10000000 - northing;
	    	}
	    	
	    	setVariables();
	    	latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / Math.PI;
	
	    	if (zone > 0) {
	    		zoneCM = 6 * zone - 183.0;
	    	} else {
	    		zoneCM = 3.0;
	    	}
	
	    	longitude = zoneCM - _a3;
	    	if (hemisphere.equals("S")) {
	    		latitude = -latitude;
	    	}
	
	    	latlon[0] = latitude;
	    	latlon[1] = longitude;
	    	return latlon;	
	    }
	
	    /**
		 * Initialize the needed variables to convert UTM to latitude, longitude
		 */
	    protected void setVariables() {
	    	
	    	arc = northing / k0;
	    	mu = arc / (a * (1 - Math.pow(e, 2) / 4.0 - 3 * Math.pow(e, 4) / 64.0 - 5 * Math.pow(e, 6) / 256.0));
	
	    	ei = (1 - Math.pow((1 - e * e), (1 / 2.0))) / (1 + Math.pow((1 - e * e), (1 / 2.0)));
	
	    	ca = 3 * ei / 2 - 27 * Math.pow(ei, 3) / 32.0;	
	    	cb = 21 * Math.pow(ei, 2) / 16 - 55 * Math.pow(ei, 4) / 32;
	    	cc = 151 * Math.pow(ei, 3) / 96;
	    	cd = 1097 * Math.pow(ei, 4) / 512;
	    	phi1 = mu + ca * Math.sin(2 * mu) + cb * Math.sin(4 * mu) + cc * Math.sin(6 * mu) + cd * Math.sin(8 * mu);
	
	    	n0 = a / Math.pow((1 - Math.pow((e * Math.sin(phi1)), 2)), (1 / 2.0));	
	    	r0 = a * (1 - e * e) / Math.pow((1 - Math.pow((e * Math.sin(phi1)), 2)), (3 / 2.0));
	    	fact1 = n0 * Math.tan(phi1) / r0;
	
	    	_a1 = 500000 - easting;
	    	dd0 = _a1 / (n0 * k0);
	    	fact2 = dd0 * dd0 / 2;
	
	    	t0 = Math.pow(Math.tan(phi1), 2);
	    	Q0 = e1sq * Math.pow(Math.cos(phi1), 2);
	    	fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * Math.pow(dd0, 4) / 24;
	
	    	fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * Math.pow(dd0, 6) / 720;

	    	lof1 = _a1 / (n0 * k0);
	    	lof2 = (1 + 2 * t0 + Q0) * Math.pow(dd0, 3) / 6.0;
	    	lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * Math.pow(Q0, 2) + 8 * e1sq + 24 * Math.pow(t0, 2)) * Math.pow(dd0, 5) / 120;
	    	_a2 = (lof1 - lof2 + lof3) / Math.cos(phi1);
	    	_a3 = _a2 * 180 / Math.PI;
	    }	    
	}
	
	
	/*** LatZones ***/
	
	private class LatZones {
		
		private static final String CHARACTERS = "CDEFGHJKLMNPQRSTUVWXY";
		
		/**
		 * Calculate the zone and the letter the given position
		 * 
		 * @param latitude - latitude coordinate
		 * @param longitude - longitude coordinate
		 * @return The zone and letter from the given position 
		 */
		public String getLatZoneLetter(double latitude, double longitude) {
			
			String zoneAndLetter = calculateZone(latitude, longitude) + " " + Character.toString(calculateLetter(latitude));
			return zoneAndLetter;
		}

		/**
		 * Calculate the zone of the given position
		 * 
		 * @param latitude - latitude coordinate
		 * @param longitude - longitude coordinate
		 * @return The corresponding zone
		 */
		private int calculateZone(double latitude, double longitude) {
			
			if((latitude >= 56.0) && (latitude < 64.0) && (longitude >= 3.0) && (longitude < 12.0))
				return 32;
			
			if((latitude >= 72.0) && (latitude < 84.0)) {
				if ((longitude >= 0.0)  && (longitude <  9.0)) {
					return 31;
				} else if((longitude >= 9.0) && (longitude < 21.0)) {
					return 33;
				} else if((longitude >= 21.0) && (longitude < 33.0)) {
					return 35;
				} else if((longitude >= 33.0) && (longitude < 42.0)) {
					return 37;
				}
			}
			
			return (int)(Math.floor((longitude + 180) / 6) + 1);
		}
		
		/**
		 * Calculate the letter associated to the latitude coordinate
		 * 
		 * @param latitude - latitude coordinate
		 * @return The corresponding letter
		 */
		private char calculateLetter(double latitude) {
			
			if((-80.0 <= latitude) && (latitude <= 84.0))
				return CHARACTERS.charAt((int	)Math.floor((latitude + 80) / 8));
			
			return 'Z';
		}
	}
}
