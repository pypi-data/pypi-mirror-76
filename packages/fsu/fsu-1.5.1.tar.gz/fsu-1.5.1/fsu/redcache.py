from functools import wraps
from msgpack import packb, unpackb

def make_redcache(get_redis, prefix="redcache"):
    redis = None

    async def get_redis_():
        nonlocal redis

        if redis is None:
            redis = await get_redis()

        return redis

    def cache(period, hash_func):
        def f(wrapped):
            @wraps(wrapped)
            async def g(*args, **kwargs):
                r = await get_redis_()

                key = f"{prefix}:{f.__module__}.{f.__qualname__}:{hash_func(*args, **kwargs)}"

                # NOTE there is a get-set issue but it donesn't matter.....
                try:
                    v = await r.get(key)
                except:
                    v = None

                if v is None:
                    v = await wrapped(*args, **kwargs)
                    try:
                        await r.set(key, packb(v), expire=period, exist="SET_IF_NOT_EXIST")
                    except:
                        pass
                else:
                    v = unpackb(v)

                return v

            return g

        return f

    return cache
