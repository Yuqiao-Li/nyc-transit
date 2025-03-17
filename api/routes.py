from flask import jsonify, request
from services.data_service import DataService


def register_routes(bp):
    """
    注册API端点到蓝图

    Args:
        bp (Blueprint): Flask蓝图对象
    """
    # 创建数据服务实例
    data_service = DataService()

    @bp.route('/feeds')
    def list_feeds():
        """列出所有可用的数据源"""
        feeds = data_service.get_available_feeds()
        return jsonify(feeds)

    @bp.route('/health')
    def health_check():
        """健康检查端点"""
        return jsonify({"status": "ok", "message": "Service is running"})

    # 地铁相关端点
    @bp.route('/subway/feeds')
    def list_subway_feeds():
        """列出所有可用的地铁数据源"""
        return jsonify(data_service.get_subway_feeds())

    @bp.route('/subway/feeds/<feed_id>')
    def get_subway_feed(feed_id):
        """获取特定地铁线路组的数据"""
        data = data_service.get_subway_feed(feed_id)
        return jsonify(data)

    # 长岛铁路相关端点
    @bp.route('/lirr/feeds/<feed_id>')
    def get_lirr_feed(feed_id):
        """获取长岛铁路数据"""
        data = data_service.get_lirr_feed(feed_id)
        return jsonify(data)

    # Metro-North相关端点
    @bp.route('/mnr/feeds/<feed_id>')
    def get_mnr_feed(feed_id):
        """获取Metro-North数据"""
        data = data_service.get_mnr_feed(feed_id)
        return jsonify(data)

    # 服务提醒相关端点
    @bp.route('/alerts/<alert_type>')
    def get_service_alerts(alert_type):
        """获取服务提醒"""
        data = data_service.get_service_alerts(alert_type)
        return jsonify(data)

    # 无障碍设施相关端点
    @bp.route('/accessibility/<data_type>')
    def get_accessibility_data(data_type):
        """获取无障碍设施数据"""
        data = data_service.get_accessibility_data(data_type)
        return jsonify(data)

    @bp.route('/accessibility/station/<station_id>')
    def get_station_accessibility(station_id):
        """获取特定车站的无障碍设施信息"""
        data = data_service.get_station_accessibility(station_id)
        return jsonify(data)