"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='redis-17524.c16.us-east-1-3.ec2.cloud.redislabs.com',
    port=17524,
    decode_responses=True,
    username="default",
    password="MXfAUiZh1WiAR6hOzqmx3WwduVish34P",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)