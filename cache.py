import json
import inspect
from base64 import b64encode
from hashlib import md5
from flask_caching import Cache, function_namespace
from settings import USE_CACHE


class ResourceCache(Cache):
    """
    When the class method is being memoized, cache key uses the class name from
    self or cls.
    """

    def _memoize_make_cache_key(
        self,
        make_name=None,
        timeout=None,
        forced_update=False,
        hash_method=md5,
        source_check=False,
        args_to_ignore=None,
    ):
        def make_cache_key(f, *args, **kwargs):
            fname, _ = function_namespace(f)

            if callable(make_name):
                altfname = make_name(fname)
            else:
                altfname = fname

            cache_key = altfname + json.dumps(
                dict(args=self._extract_self_arg(f, args), kwargs=kwargs),
                sort_keys=True,
            )
            cache_key = md5(cache_key.encode("utf-8"))
            cache_key = b64encode(cache_key.digest())
            cache_key = cache_key[:16].decode("utf-8")
            return cache_key

        return make_cache_key

    @staticmethod
    def _extract_self_arg(f, args):
        argspec_args = inspect.getargspec(f).args

        if argspec_args and argspec_args[0] in ("self", "cls"):
            if hasattr(args[0], "__name__"):
                return (args[0].__name__,) + args[1:]
            return (args[0].__class__.__name__,) + args[1:]
        return args


cache_config = {
    "CACHE_TYPE": "null",
    "CACHE_KEY_PREFIX": "todo",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": "6379",
    "CACHE_REDIS_URL": "redis://localhost:6379",
}

if USE_CACHE:
    cache_config["CACHE_TYPE"] = "redis"

cache = Cache(config=cache_config)
resource_cache = ResourceCache(config=cache_config)
