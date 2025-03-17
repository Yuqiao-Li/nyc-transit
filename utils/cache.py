import time


class SimpleCache:
    """
    简单的内存缓存实现
    """

    def __init__(self):
        self.cache = {}  # 存储缓存数据
        self.timestamps = {}  # 存储时间戳

    def get(self, key, timeout=60):
        """
        获取缓存数据

        Args:
            key (str): 缓存键
            timeout (int): 超时时间(秒)

        Returns:
            any: 缓存的数据，如果不存在或已过期则返回None
        """
        # 检查键是否存在
        if key not in self.cache:
            return None

        # 检查是否过期
        current_time = time.time()
        if current_time - self.timestamps[key] > timeout:
            # 移除过期数据
            self.remove(key)
            return None

        return self.cache[key]

    def set(self, key, value):
        """
        设置缓存数据

        Args:
            key (str): 缓存键
            value (any): 要缓存的数据
        """
        self.cache[key] = value
        self.timestamps[key] = time.time()

    def remove(self, key):
        """
        删除特定缓存

        Args:
            key (str): 要删除的缓存键
        """
        if key in self.cache:
            del self.cache[key]
            del self.timestamps[key]

    def clear(self):
        """清除所有缓存"""
        self.cache = {}
        self.timestamps = {}

    def get_stats(self):
        """
        获取缓存统计信息

        Returns:
            dict: 包含缓存统计信息的字典
        """
        return {
            "total_keys": len(self.cache),
            "keys": list(self.cache.keys())
        }


# 创建全局缓存实例
cache = SimpleCache()