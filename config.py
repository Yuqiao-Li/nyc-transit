"""应用配置"""

# 数据源URLs
SUBWAY_FEEDS = {
    'ace': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace',
    'bdfm': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm',
    'g' :'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g',
    'jz' : 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz',
    'nqrw': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw',
    'l':'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l',
    'num_s':'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs',
    'sir': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si'
    # ...其他线路...
}

LIRR_FEEDS = {
    'lirr': ' https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/lirr%2Fgtfs-lirr'
}

MNR_FEEDS = {
    'mnr':'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr'
}

SERVICE_ALERT_FEEDS = {
    'all_alerts':'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fall-alerts',
    'subway_alerts':'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts',
    'bus_alerts':'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fbus-alerts',
    'lirr_alerts':'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Flirr-alerts',
    'mnr_alerts': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fmnr-alerts'
}
# 无障碍设施数据源
ELEVATOR_ESCALATOR_FEEDS = {
    'current':"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fnyct_ene.json",
    'upcoming':'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fnyct_ene_upcoming.json',
    'equipment':'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fnyct_ene_equipments.json'

}

# 缓存设置
CACHE_TIMEOUT = {
    # 类别默认值
    'subway_default': 30,      # 地铁数据默认缓存30秒
    'lirr_default': 60,        # 长岛铁路数据默认缓存1分钟
    'mnr_default': 60,         # Metro-North数据默认缓存1分钟
    'alerts_default': 180,     # 服务提醒默认缓存3分钟
    'accessibility_default': 300,  # 无障碍设施数据默认缓存5分钟

    # 特定覆盖 - 如果需要为特定数据源设置不同的超时时间
    'lirr_alerts': 300,        # 长岛铁路提醒缓存5分钟
    'mnr_alerts': 300,         # Metro-North提醒缓存5分钟
    'upcoming': 1800,          # 计划中的电梯/自动扶梯维护信息缓存30分钟
    'equipment': 3600          # 设备信息缓存1小时
}