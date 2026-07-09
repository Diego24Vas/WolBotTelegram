import os


_version_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "VERSION")
with open(_version_path) as f:
    __version__ = f.read().strip()