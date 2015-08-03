package geoprojection

import grails.rest.RestfulController
import grails.transaction.Transactional
import org.apache.commons.logging.LogFactory

import geoJava.KMLCircle

@Transactional(readOnly = true)
class CircleController extends RestfulController {

    static responseFormats = ['json']
    private static final log = LogFactory.getLog(this)

    def point() {

        log.debug 'circlePointGenerator'

        def jsonReq = request.JSON
        log.debug jsonReq

        Circle circle = new Circle()
        circle.radius = jsonReq.radius
        circle.lat = jsonReq.lat
        circle.lon = jsonReq.lon
        circle. altitude = jsonReq.altitude

        def circlePoints = KMLCircle.genCircle(circle)

        def response = [points: circlePoints]
        respond response
    }
}
