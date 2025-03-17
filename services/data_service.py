import requests
import datetime
from google.transit import gtfs_realtime_pb2
from config import (
    SUBWAY_FEEDS, LIRR_FEEDS, MNR_FEEDS,
    SERVICE_ALERT_FEEDS, ELEVATOR_ESCALATOR_FEEDS,
    CACHE_TIMEOUT
)
from utils.cache import cache


class DataService:
    """
    数据服务类 - 处理所有数据获取和处理
    """

    def get_cache_timeout(self, category, item_id):
        """
        获取特定项目的缓存超时时间

        Args:
            category (str): 类别 ('subway', 'lirr', 'mnr', 'alerts', 'accessibility')
            item_id (str): 项目ID

        Returns:
            int: 缓存超时时间(秒)
        """
        # 先检查是否有特定项目的超时设置
        specific_key = f"{item_id}"
        if specific_key in CACHE_TIMEOUT:
            return CACHE_TIMEOUT[specific_key]

        # 然后检查是否有特定类别的默认超时设置
        category_key = f"{category}_default"
        if category_key in CACHE_TIMEOUT:
            return CACHE_TIMEOUT[category_key]

        # 最后返回全局默认值
        return 60  # 默认1分钟

    def get_available_feeds(self):
        """
        获取所有可用的数据源

        Returns:
            dict: 数据源类型和ID的字典
        """
        return {
            "subway": list(SUBWAY_FEEDS.keys()),
            "lirr": list(LIRR_FEEDS.keys()),
            "mnr": list(MNR_FEEDS.keys()),
            "alerts": list(SERVICE_ALERT_FEEDS.keys()),
            "accessibility": list(ELEVATOR_ESCALATOR_FEEDS.keys())
        }

    def get_subway_feeds(self):
        """
        获取所有可用的地铁数据源

        Returns:
            dict: 地铁数据源ID和URL的字典
        """
        return SUBWAY_FEEDS

    def parse_gtfs_rt(self, content, feed_id):
        """
        解析GTFS-RT数据

        Args:
            content (bytes): GTFS-RT二进制内容
            feed_id (str): 数据源ID

        Returns:
            dict: 解析后的数据
        """
        try:
            # 解析GTFS-RT数据
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(content)

            # 转换为可JSON化的格式
            result = {
                "header": {
                    "timestamp": feed.header.timestamp,
                    "human_time": datetime.datetime.fromtimestamp(feed.header.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                    "feed_id": feed_id
                },
                "entities": []
            }

            # 处理每个实体(车辆、行程更新、提醒等)
            for entity in feed.entity:
                entity_data = {"id": entity.id}

                # 处理车辆位置
                if entity.HasField('vehicle'):
                    vehicle = entity.vehicle
                    vehicle_data = {
                        "trip": {
                            "trip_id": vehicle.trip.trip_id,
                            "route_id": vehicle.trip.route_id
                        },
                        "timestamp": vehicle.timestamp
                    }

                    if vehicle.timestamp:
                        vehicle_data["human_time"] = datetime.datetime.fromtimestamp(vehicle.timestamp).strftime(
                            '%Y-%m-%d %H:%M:%S')

                    if vehicle.HasField('position'):
                        vehicle_data["position"] = {
                            "latitude": vehicle.position.latitude,
                            "longitude": vehicle.position.longitude
                        }

                        if vehicle.position.HasField('bearing'):
                            vehicle_data["position"]["bearing"] = vehicle.position.bearing

                        if vehicle.position.HasField('speed'):
                            vehicle_data["position"]["speed"] = vehicle.position.speed

                    if vehicle.HasField('current_status'):
                        status_mapping = {
                            0: "INCOMING_AT",
                            1: "STOPPED_AT",
                            2: "IN_TRANSIT_TO"
                        }
                        vehicle_data["current_status"] = status_mapping.get(vehicle.current_status, "UNKNOWN")

                    if vehicle.HasField('stop_id'):
                        vehicle_data["stop_id"] = vehicle.stop_id

                    entity_data["vehicle"] = vehicle_data

                # 处理行程更新
                if entity.HasField('trip_update'):
                    trip_update = entity.trip_update
                    update_data = {
                        "trip": {
                            "trip_id": trip_update.trip.trip_id,
                            "route_id": trip_update.trip.route_id
                        },
                        "stop_time_updates": []
                    }

                    if trip_update.HasField('timestamp'):
                        update_data["timestamp"] = trip_update.timestamp
                        update_data["human_time"] = datetime.datetime.fromtimestamp(trip_update.timestamp).strftime(
                            '%Y-%m-%d %H:%M:%S')

                    for stop_time in trip_update.stop_time_update:
                        stop_data = {"stop_id": stop_time.stop_id}

                        if stop_time.HasField('arrival'):
                            arrival_data = {"time": stop_time.arrival.time}

                            if stop_time.arrival.time:
                                arrival_data["human_time"] = datetime.datetime.fromtimestamp(
                                    stop_time.arrival.time).strftime('%Y-%m-%d %H:%M:%S')

                            if stop_time.arrival.HasField('delay'):
                                arrival_data["delay"] = stop_time.arrival.delay

                            stop_data["arrival"] = arrival_data

                        if stop_time.HasField('departure'):
                            departure_data = {"time": stop_time.departure.time}

                            if stop_time.departure.time:
                                departure_data["human_time"] = datetime.datetime.fromtimestamp(
                                    stop_time.departure.time).strftime('%Y-%m-%d %H:%M:%S')

                            if stop_time.departure.HasField('delay'):
                                departure_data["delay"] = stop_time.departure.delay

                            stop_data["departure"] = departure_data

                        update_data["stop_time_updates"].append(stop_data)

                    entity_data["trip_update"] = update_data

                # 处理提醒
                if entity.HasField('alert'):
                    alert = entity.alert
                    alert_data = {
                        "active_period": [],
                        "informed_entity": []
                    }

                    # 添加基本信息
                    if alert.HasField('cause'):
                        alert_data["cause"] = alert.cause

                    if alert.HasField('effect'):
                        alert_data["effect"] = alert.effect

                    # 处理URL
                    if alert.HasField('url') and alert.url.translation:
                        alert_data["url"] = alert.url.translation[0].text

                    # 处理标题和描述
                    if alert.HasField('header_text') and alert.header_text.translation:
                        alert_data["header_text"] = alert.header_text.translation[0].text

                    if alert.HasField('description_text') and alert.description_text.translation:
                        alert_data["description_text"] = alert.description_text.translation[0].text

                    # 处理有效期
                    for period in alert.active_period:
                        period_data = {}

                        if period.HasField('start'):
                            period_data["start"] = {
                                "timestamp": period.start,
                                "human_time": datetime.datetime.fromtimestamp(period.start).strftime(
                                    '%Y-%m-%d %H:%M:%S')
                            }

                        if period.HasField('end'):
                            period_data["end"] = {
                                "timestamp": period.end,
                                "human_time": datetime.datetime.fromtimestamp(period.end).strftime('%Y-%m-%d %H:%M:%S')
                            }

                        alert_data["active_period"].append(period_data)

                    # 处理影响实体
                    for entity in alert.informed_entity:
                        entity_info = {}

                        if entity.HasField('agency_id'):
                            entity_info["agency_id"] = entity.agency_id

                        if entity.HasField('route_id'):
                            entity_info["route_id"] = entity.route_id

                        if entity.HasField('route_type'):
                            entity_info["route_type"] = entity.route_type

                        if entity.HasField('stop_id'):
                            entity_info["stop_id"] = entity.stop_id

                        alert_data["informed_entity"].append(entity_info)

                    entity_data["alert"] = alert_data

                result["entities"].append(entity_data)

            return result

        except Exception as e:
            return {"error": f"Error parsing GTFS-RT data: {str(e)}"}

    def get_subway_feed(self, feed_id):
        """
        获取特定地铁线路组的数据

        Args:
            feed_id (str): 地铁线路组ID

        Returns:
            dict: 处理后的地铁数据或错误信息
        """
        # 验证feed_id
        if feed_id not in SUBWAY_FEEDS:
            return {"error": f"Invalid subway feed: {feed_id}"}

        # 检查缓存
        cache_key = f"subway_{feed_id}"
        cached_data = cache.get(cache_key, self.get_cache_timeout('subway', feed_id))
        if cached_data:
            return cached_data

        # 获取数据
        try:
            response = requests.get(SUBWAY_FEEDS[feed_id])

            if response.status_code == 200:
                # 解析GTFS-RT数据
                result = self.parse_gtfs_rt(response.content, feed_id)

                # 缓存结果
                cache.set(cache_key, result)
                return result
            else:
                return {"error": f"HTTP error: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def get_lirr_feed(self, feed_id):
        """
        获取长岛铁路数据

        Args:
            feed_id (str): 长岛铁路数据源ID

        Returns:
            dict: 处理后的长岛铁路数据或错误信息
        """
        # 验证feed_id
        if feed_id not in LIRR_FEEDS:
            return {"error": f"Invalid LIRR feed: {feed_id}"}

        # 检查缓存
        cache_key = f"lirr_{feed_id}"
        cached_data = cache.get(cache_key, self.get_cache_timeout('lirr', feed_id))
        if cached_data:
            return cached_data

        # 获取数据
        try:
            response = requests.get(LIRR_FEEDS[feed_id])

            if response.status_code == 200:
                # 解析GTFS-RT数据
                result = self.parse_gtfs_rt(response.content, feed_id)

                # 缓存结果
                cache.set(cache_key, result)
                return result
            else:
                return {"error": f"HTTP error: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def get_mnr_feed(self, feed_id):
        """
        获取Metro-North数据

        Args:
            feed_id (str): Metro-North数据源ID

        Returns:
            dict: 处理后的Metro-North数据或错误信息
        """
        # 验证feed_id
        if feed_id not in MNR_FEEDS:
            return {"error": f"Invalid MNR feed: {feed_id}"}

        # 检查缓存
        cache_key = f"mnr_{feed_id}"
        cached_data = cache.get(cache_key, self.get_cache_timeout('mnr', feed_id))
        if cached_data:
            return cached_data

        # 获取数据
        try:
            response = requests.get(MNR_FEEDS[feed_id])

            if response.status_code == 200:
                # 解析GTFS-RT数据
                result = self.parse_gtfs_rt(response.content, feed_id)

                # 缓存结果
                cache.set(cache_key, result)
                return result
            else:
                return {"error": f"HTTP error: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def get_service_alerts(self, alert_type):
        """
        获取服务提醒数据

        Args:
            alert_type (str): 提醒类型

        Returns:
            dict: 服务提醒数据或错误信息
        """
        # 验证alert_type
        if alert_type not in SERVICE_ALERT_FEEDS:
            return {"error": f"Invalid alert type: {alert_type}"}

        # 检查缓存
        cache_key = f"alert_{alert_type}"
        cached_data = cache.get(cache_key, self.get_cache_timeout('alerts', alert_type))
        if cached_data:
            return cached_data

        # 获取数据
        try:
            response = requests.get(SERVICE_ALERT_FEEDS[alert_type])

            if response.status_code == 200:
                # 解析GTFS-RT数据
                result = self.parse_gtfs_rt(response.content, alert_type)

                # 缓存结果
                cache.set(cache_key, result)
                return result
            else:
                return {"error": f"HTTP error: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def get_accessibility_data(self, data_type):
        """
        获取无障碍设施数据

        Args:
            data_type (str): 数据类型 ('current', 'upcoming', 'equipment')

        Returns:
            dict: 无障碍设施数据或错误信息
        """
        # 验证数据类型
        if data_type not in ELEVATOR_ESCALATOR_FEEDS:
            return {"error": f"Invalid accessibility data type: {data_type}"}

        # 检查缓存
        cache_key = f"accessibility_{data_type}"
        cached_data = cache.get(cache_key, self.get_cache_timeout('accessibility', data_type))
        if cached_data:
            return cached_data

        # 获取数据
        try:
            response = requests.get(ELEVATOR_ESCALATOR_FEEDS[data_type])

            if response.status_code == 200:
                data = response.json()
                # 缓存结果
                cache.set(cache_key, data)
                return data
            else:
                return {"error": f"HTTP error: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def get_station_accessibility(self, station_id):
        """
        获取特定车站的无障碍设施信息

        Args:
            station_id (str): 车站ID

        Returns:
            dict: 车站无障碍设施信息
        """
        # 获取设备信息
        equipment_data = self.get_accessibility_data('equipment')

        # 检查是否有错误
        if "error" in equipment_data:
            return equipment_data

        # 筛选特定车站的设备
        # 注意：这里需要根据实际的数据结构调整
        station_equipment = []

        # 假设equipment_data是一个字典，包含一个equipment列表
        if "equipment" in equipment_data:
            for item in equipment_data["equipment"]:
                if item.get("station_id") == station_id:
                    station_equipment.append(item)

        # 返回结果
        return {
            "station_id": station_id,
            "equipment_count": len(station_equipment),
            "equipment": station_equipment
        }

