# -*- coding: utf-8 -*-
# @Time    : 2024/12/8 17:49
# @Author  : nongbin
# @FileName: redis_dao.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

import redis
from typing import Set, Optional

from config.config import Config


class RedisDao(object):
    def __init__(self):
        # Initialize Redis connection
        self._redis_client = redis.Redis(
            host=Config.get_instance().get_with_nested_params("database", "redis", "host"),
            port=Config.get_instance().get_with_nested_params("database", "redis", "port"),
            password=Config.get_instance().get_with_nested_params("database", "redis", "password"),
            decode_responses=True
        )

    def add_to_set(self, set_key: str, *values: str) -> int:
        """
        Add one or more values to a set
        Returns number of elements added
        """
        return self._redis_client.sadd(set_key, *values)

    def remove_from_set(self, set_key: str, *values: str) -> int:
        """
        Remove one or more values from a set
        Returns number of elements removed
        """
        return self._redis_client.srem(set_key, *values)

    def get_set_members(self, set_key: str) -> Set[str]:
        """
        Get all members of a set
        """
        return self._redis_client.smembers(set_key)

    def is_member(self, set_key: str, value: str) -> bool:
        """
        Check if value exists in set
        """
        result = self._redis_client.sismember(set_key, value)
        return bool(result)
    def get_set_size(self, set_key: str) -> int:
        """
        Get number of members in a set
        """
        return self._redis_client.scard(set_key)

    def delete_set(self, set_key: str) -> bool:
        """
        Delete entire set
        Returns True if set was deleted, False if key didn't exist
        """
        return bool(self._redis_client.delete(set_key))

    def get_random_member(self, set_key: str) -> Optional[str]:
        """
        Get random member from set without removing it
        """
        return self._redis_client.srandmember(set_key)

    def pop_random_member(self, set_key: str) -> Optional[str]:
        """
        Remove and return random member from set
        """
        return self._redis_client.spop(set_key)

    def set_expiration(self, key: str, expiration_seconds: int) -> None:
        """
        Set the expiration time for a key in seconds
        Returns True if successful, False otherwise
        """
        self._redis_client.expire(key, expiration_seconds)

    def delete_key(self, key: str) -> None:
        """
        Delete a key from Redis
        """
        self._redis_client.delete(key)
    def get_set_ttl(self, set_key: str) -> str:
        """
        Get the remaining TTL (Time To Live) in minutes:seconds format for a given set key.
        
        Args:
            set_key (str): The key of the set to check
            
        Returns:
            str: The remaining time to live in MM:SS format. Returns:
                 "-2:00" if the key does not exist
                 "-1:00" if the key exists but has no associated expire
                 Otherwise, returns the remaining TTL in MM:SS format
        """
        ttl = self._redis_client.ttl(set_key)
        if ttl < 0:
            return f"{ttl}:00"
        minutes = ttl // 60
        seconds = ttl % 60
        return f"{minutes:02d}:{seconds:02d}"

    def set_key_with_expiration(self, key: str, *values: str, expiration_seconds: int) -> bool:
        """
        Set a new key with values and expiration if the key doesn't exist.
        
        Args:
            key (str): The key to set
            *values (str): One or more values to add to the set
            expiration_seconds (int): The expiration time in seconds
            
        Returns:
            bool: True if the key was set with expiration, False if the key already exists
        """
        # Check if key exists
        if self._redis_client.exists(key):
            return False
            
        # Add values to set
        self._redis_client.sadd(key, *values)
        # Set expiration
        self._redis_client.expire(key, expiration_seconds)
        return True

    def has_expiration(self, key: str) -> bool:
        """
        Check if a key has an expiration set.
        
        Args:
            key (str): The key to check
            
        Returns:
            bool: True if the key exists and has an expiration set,
                 False if the key doesn't exist or has no expiration
        """
        ttl = self._redis_client.ttl(key)
        # ttl > 0 means key exists and has expiration
        # ttl == -1 means key exists but has no expiration
        # ttl == -2 means key doesn't exist
        return ttl > 0