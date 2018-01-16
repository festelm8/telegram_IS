"""General project utils."""

def get_config(name):
    """get value from top level config.py"""

    return getattr(__import__('instance.config',
                              fromlist=[name]),
                   name)
