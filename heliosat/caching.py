# -*- coding: utf-8 -*-

"""smoothing.py

Implements simple caching functionality.
"""

import hashlib
import json
import logging
import os
import pickle

import heliosat


def generate_cache_key(identifiers):
    """Generate SHA256 digest from dictionary json dump which acts as key for cached data.

    Parameters
    ----------
    identifiers : dict
        dictionary containing cache identifiers

    Returns
    -------
    str
        cache key (SHA256 digest)
    """
    hashobj = hashlib.sha256()
    hashobj.update(json.dumps(identifiers, sort_keys=True).encode("utf-8"))

    return hashobj.hexdigest()


def delete_cache_entry(key):
    """Delete cached entry belonging to specified key.

    Parameters
    ----------
    key : str
        cache key

    Raises
    ------
    KeyError
        if no entry for the given key is found
    """
    logger = logging.getLogger(__name__)

    cache_path = heliosat._paths["cache"]

    if not cache_entry_exists(key):
        logger.exception("cache key \"%s\" does not exist", key)
        raise KeyError("cache key \"%s\" does not exist", key)

    os.remove(os.path.join(cache_path, "{0}.cache".format(key)))


def get_cache_entry(key):
    """Retrieve cache entry specified by key.

    Parameters
    ----------
    key : str
        cache key

    Returns
    -------
    str
        data object

    Raises
    ------
    KeyError
        if no entry for the given key is found
    """
    logger = logging.getLogger(__name__)

    cache_path = heliosat._paths["cache"]

    if not cache_entry_exists(key):
        logger.exception("cache key \"%s\" does not exist", key)
        raise KeyError("cache key \"%s\" does not exist", key)

    with open(os.path.join(cache_path, "{0}.cache".format(key)), "rb") as pickle_file:
        cache_data = pickle.load(pickle_file)

    return cache_data


def cache_entry_exists(key):
    """Check if an entry for the given cache key exists.

    Parameters
    ----------
    key : str
        cache key

    Returns
    -------
    bool
        if key exists
    """
    cache_path = heliosat._paths["cache"]

    return os.path.exists(os.path.join(cache_path, "{}.cache".format(key)))


def set_cache_entry(key, obj):
    """Store data in cache using specified key.

    Parameters
    ----------
    key : str
        cache key
    obj : object
        data object
    """
    cache_path = heliosat._paths["cache"]

    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    with open(os.path.join(cache_path, "{}.cache".format(key)), "wb") as pickle_file:
        pickle.dump(obj, pickle_file)