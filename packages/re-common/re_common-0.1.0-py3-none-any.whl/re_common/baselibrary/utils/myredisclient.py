import sys
import time

import redis
from redis.client import Pipeline, Redis

from re_common.baselibrary import IniConfig


class MyRedis(object):
    def __init__(self, configpath=""):
        self.configpath = configpath

    def set_configpath(self, configpath):
        self.configpath = configpath

    def set_redis_from_config(self, sesc="proxy", encoding="utf-8"):
        """
        设置 redis的配置信息
        :param sesc: 选择配置文件里的字典信息
        :param encoding: 编码
        :return:
        """
        assert self.configpath != "", 'configpath 为空，请调用set_configpath'
        dictsall = IniConfig(self.configpath).get_conf_dict(encoding=encoding)
        dicts = dictsall[sesc]
        self.RedisHost = dicts['RedisHost']
        self.RedisPort = dicts['RedisPort']
        self.RedisDB = dicts['RedisDB']
        self.RedisKey = dicts['RedisKey']

    def conn_redis(self):
        """
        链接 设置好的配置文件的redis
        :return: 返回一个 connect
        """
        assert self.RedisHost, 'RedisHost 不存在，请先调用set_redis_from_config'
        assert self.RedisPort, 'RedisPort 不存在，请先调用set_redis_from_config'
        assert self.RedisDB, 'RedisDB 不存在，请先调用set_redis_from_config'
        assert self.RedisKey, 'RedisKey 不存在，请先调用set_redis_from_config'
        self.rconn = redis.StrictRedis(host=self.RedisHost, port=self.RedisPort, db=self.RedisDB, decode_responses=True)
        return self.rconn

    def getDataFromRedis(self):
        """
        获取 信息
        :return: 一个可迭代的数据
        """
        assert self.RedisKey, 'RedisKey 不存在，请先调用set_redis_from_config'
        assert self.rconn, 'rconn 不存在，请先调用conn_redis'
        if self.rconn:
            rows = self.rconn.smembers(self.RedisKey)
            return rows
        else:
            print("redis出现连接错误")
            sys.exit(-1)

    def get_pipeline(self):
        """
        获取一个通道，便于批量删除和增加（节约时耗）
        :return: pipeline()
        """
        assert isinstance(self.rconn, Redis), Exception("请调用conn_redis获取")
        self.pipe = self.rconn.pipeline()
        return self.pipe

    def delete(self, RedisKey):
        """
        删除一个RedisKey
        :param RedisKey: 需要删除的RedisKey
        :return:
        """
        assert isinstance(self.pipe, Pipeline), Exception("请调用get_pipeline获取")
        self.pipe.delete(RedisKey)

    def sadd(self, name, ProxyPoolValid: set):
        """
        增加 一个 set集合
        :param name: 需要增加的rediskey
        :param ProxyPoolValid: 传入集合
        :return:
        """
        assert isinstance(self.pipe, Pipeline), Exception("请调用get_pipeline获取")
        self.pipe.sadd(name, *ProxyPoolValid)
        self.pipe.execute()

    def hset(self, name, key, value):
        """
        以hash 散列表的形式存储
        :param name:
        :param key:
        :param value:
        :return:
        """
        assert isinstance(self.pipe, Pipeline), Exception("请调用get_pipeline获取")
        self.pipe.hset(name, key, value)
        self.pipe.execute()

    def hget(self, name, key):
        """
        以hash 散列表的形式取出
        :param name:
        :param key:
        :return:
        """
        assert isinstance(self.pipe, Pipeline), Exception("请调用get_pipeline获取")
        self.pipe.hget(name, key)
        self.pipe.execute()

    def set(self, name, value):
        """
        写入
        :param name:
        :param value:
        :return:
        """
        self.rconn.set(name, value)

    def get(self, name):
        """
        取出
        :param name:
        :return:
        """
        return self.rconn.get(name)


def RedisConnect(configpath, sesc="proxy", encoding="utf-8"):
    """
    连接数据库 通过读取配置文件连接,如果读取配置文件 失败  返回None
    :return:
    """
    dictsall = IniConfig(configpath).get_conf_dict(encoding=encoding)
    dicts = dictsall[sesc]
    RedisHost = dicts['RedisHost']
    RedisPort = dicts['RedisPort']
    RedisDB = dicts['RedisDB']
    RedisKey = dicts['RedisKey']
    try:
        rconn = redis.StrictRedis(host=RedisHost, port=RedisPort, db=RedisDB, decode_responses=True)
    except:
        # 有可能因为网络波动无法连接 这里休眠10秒重连一次  如果还是失败就放弃
        time.sleep(10)
        rconn = redis.StrictRedis(host=RedisHost, port=RedisPort, db=RedisDB, decode_responses=True)
    if rconn:
        return rconn, RedisKey
    return None


def getDataFromRedis(configpath, sesc="proxy"):
    """
    取出数据
    :param configpath:
    :param sesc:
    :return:
    """
    rconn, RedisKey = RedisConnect(configpath, sesc=sesc)
    if rconn:
        rows = rconn.smembers(RedisKey)
        return rows
    else:
        print("redis出现连接错误")
        sys.exit(-1)
