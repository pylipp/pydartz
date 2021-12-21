try:
    from importlib import metadata as importlib_metadata
except ImportError:
    import importlib_metadata


__version__ = importlib_metadata.version(__package__)
