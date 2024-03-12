try:
    from .local import *  # noqa: F403, F401
except ImportError:
    from .base import *  # noqa: F403, F401
