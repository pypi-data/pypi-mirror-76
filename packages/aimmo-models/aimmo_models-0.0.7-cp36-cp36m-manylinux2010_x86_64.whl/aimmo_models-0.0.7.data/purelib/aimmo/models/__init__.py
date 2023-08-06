"""Deep learning model deployment helper package"""
from pkg_resources import get_distribution

from .model import Model
from .server import Server

__version__ = get_distribution("aimmo-models").version
