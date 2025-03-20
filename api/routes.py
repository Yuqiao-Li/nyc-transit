from flask import jsonify, request
from services.data_service import DataService


def register_routes(bp):

   # Initialize data service
   data_service = DataService()

   @bp.route('/feeds')
   def list_feeds():
       """List all available data feeds"""
       feeds = data_service.get_available_feeds()
       return jsonify(feeds)

   @bp.route('/health')
   def health_check():
       """Health check endpoint"""
       return jsonify({"status": "ok", "message": "Service is running"})

   # Subway endpoints
   @bp.route('/subway/feeds')
   def list_subway_feeds():
       """List all available subway feeds"""
       return jsonify(data_service.get_subway_feeds())

   @bp.route('/subway/feeds/<feed_id>')
   def get_subway_feed(feed_id):
       """Get data for specific subway feed"""
       data = data_service.get_subway_feed(feed_id)
       return jsonify(data)

   # LIRR endpoints
   @bp.route('/lirr/feeds/<feed_id>')
   def get_lirr_feed(feed_id):
       """Get LIRR data"""
       data = data_service.get_lirr_feed(feed_id)
       return jsonify(data)

   # Metro-North endpoints
   @bp.route('/mnr/feeds/<feed_id>')
   def get_mnr_feed(feed_id):
       """Get Metro-North data"""
       data = data_service.get_mnr_feed(feed_id)
       return jsonify(data)

   # Service alert endpoints
   @bp.route('/alerts/<alert_type>')
   def get_service_alerts(alert_type):
       """Get service alerts"""
       data = data_service.get_service_alerts(alert_type)
       return jsonify(data)

   # Accessibility endpoints
   @bp.route('/accessibility/<data_type>')
   def get_accessibility_data(data_type):
       """Get accessibility data"""
       data = data_service.get_accessibility_data(data_type)
       return jsonify(data)

   @bp.route('/accessibility/station/<station_id>')
   def get_station_accessibility(station_id):
       """Get station accessibility info"""
       data = data_service.get_station_accessibility(station_id)
       return jsonify(data)

   @bp.route('/stations')
   def list_stations():
       """List all stations"""
       stations = data_service.get_stations()
       return jsonify(stations)

   @bp.route('/routes')
   def list_routes():
       """List all routes"""
       routes = data_service.get_routes()
       return jsonify(routes)

   @bp.route('/routes/<route_id>/shape')
   def get_route_shape(route_id):
       """Get shape for a specific route"""
       shape_data = data_service.get_line_shape(route_id)
       return jsonify(shape_data)

   @bp.route('/routes/<route_id>/stops')
   def get_route_stops(route_id):
       """Get stops for a specific route"""
       stops_data = data_service.get_stops_for_route(route_id)
       return jsonify(stops_data)

   @bp.route('/line/<line_id>')
   def get_line(line_id):
       """Get line coordinates"""
       line_data = data_service.get_line(line_id)
       return jsonify(line_data)