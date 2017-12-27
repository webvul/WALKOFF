import logging

from apps.appcache import AppCache
from apps.devicedb import get_app as get_db_app
from walkoff.core.decorators import *

_logger = logging.getLogger(__name__)


class App(object):
    """Base class for apps

    Attributes:
        app (apps.devicedb.App): The ORM of the App with the name passed into the constructor
        device (apps.devicedb.Device): The ORM of the device with the ID passed into teh constructor
        device_fields (dict): A dict of the plaintext fields of the device
        device_type (str): The type of device associated with self.device

    Args:
        app (str): The name of the app
        device (int): The ID of the device
    """

    _is_walkoff_app = True

    def __init__(self, app, device):
        self.app = get_db_app(app)
        self.device = self.app.get_device(device) if (self.app is not None and device) else None
        if self.device is not None:
            self.device_fields = self.device.get_plaintext_fields()
            self.device_type = self.device.type
        else:
            self.device_fields = {}
            self.device_type = None
        self.device_id = device

    def get_all_devices(self):
        """Gets all the devices associated with this app

        Returns:
            list: A list of apps.appdevice.Device objects associated with this app
        """
        return list(self.app.devices) if self.app is not None else []

    def shutdown(self):
        """When implemented, this method performs shutdown procedures for the app
        """
        pass


_cache = AppCache()


def get_app(app_name):
    """Gets the app class for a given app from the global cache.

    Args:
        app_name (str): Name of the app to get

    Returns:
        (cls) The app's class

    Raises:
        UnknownApp: If app has only global actions or app is not found
    """
    return _cache.get_app(app_name)


def get_all_actions_for_app(app_name):
    """Gets all the names of the actions for a given app from the global cache

    Args:
        app_name (str): Name of the app

    Returns:
        (list[str]): The actions associated with the app

    Raises:
        UnknownApp: If the app is not found in the cache
    """
    return _cache.get_app_action_names(app_name)


def get_app_action(app_name, action_name):
    """Gets the action function for a given app and action name from the global cache

    Args:
        app_name (str): Name of the app
        action_name(str): Name of the action

    Returns:
        (func) The action

    Raises:
        UnknownApp: If the app is not found in the cache
        UnknownAppAction: If the app does not have the action
    """
    return _cache.get_app_action(app_name, action_name)


def get_condition(app_name, condition_name):
    """Gets the condition function for a given app and condition name from the global cache

    Args:
        app_name (str): Name of the app
        condition_name(str): Name of the action

    Returns:
        (func) The action

    Raises:
        UnknownApp: If the app is not found in the cache
        UnknownCondition: If the app does not have the condition
    """
    return _cache.get_app_condition(app_name, condition_name)


def get_all_conditions_for_app(app_name):
    """Gets all the names of the conditions for a given app from the global cache

    Args:
        app_name (str): Name of the app

    Returns:
        (list[str]): The conditions associated with the app

    Raises:
        UnknownApp: If the app is not found in the cache
    """
    return _cache.get_app_condition_names(app_name)


def get_transform(app_name, transform_name):
    """Gets the transform function for a given app and transform name from the global cache

    Args:
        app_name (str): Name of the app
        transform_name(str): Name of the transform

    Returns:
        (func) The action

    Raises:
        UnknownApp: If the app is not found in the cache
        UnknownCondition: If the app does not have the transform
    """
    return _cache.get_app_transform(app_name, transform_name)


def get_all_transforms_for_app(app_name):
    """Gets all the names of the transforms for a given app from the global cache

    Args:
        app_name (str): Name of the app

    Returns:
        (list[str]): The transforms associated with the app

    Raises:
        UnknownApp: If the app is not found in the cache
    """
    return _cache.get_app_transform_names(app_name)


def cache_apps(path):
    """Cache apps from a given path into the global cache

    Args:
        path (str): Path to apps module
    """
    _cache.cache_apps(path)


def clear_cache():
    """Clears the global cache
    """
    _cache.clear()


def is_app_action_bound(app_name, action_name):
    """Determines if the action in the global cache is bound (meaning it's inside a class) or not

    Args:
        app_name (str): Name of the app
        action_name(str): Name of the action

    Returns:
        (bool) Is the action bound?

    Raises:
        UnknownApp: If the app is not found in the cache
        UnknownAppAction: If the app does not have the action
    """
    return _cache.is_app_action_bound(app_name, action_name)
