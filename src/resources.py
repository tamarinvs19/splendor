"""Resource models."""

from dataclasses import dataclass

from multiset import Multiset


@dataclass
class Resource(object):
    pass


class Emerald(Resource):
    pass


class Sapphire(Resource):
    pass


class Ruby(Resource):
    pass


class Diamond(Resource):
    pass


class Onyx(Resource):
    pass


class Gold(Resource):
    pass


class ResourceCollection(Multiset):
    pass
