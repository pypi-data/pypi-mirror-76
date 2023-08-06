# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stormlock', 'stormlock.backends']

package_data = \
{'': ['*']}

extras_require = \
{'dynamodb': ['boto3>=1.13.1,<2.0.0'],
 'etcd': ['etcd3>=0.12.0,<0.13.0'],
 'mysql': ['mysql-connector-python>=8.0.21,<9.0.0'],
 'postgresql': ['psycopg2>=2.8.5,<3.0.0'],
 'redis': ['redis>=3.4.1,<4.0.0']}

entry_points = \
{'console_scripts': ['stormlock = stormlock.cli:run'],
 'stormlock.backends': ['dynamodb = stormlock.backends.dynamodb:DynamoDB '
                        '[dynamodb]',
                        'etcd = stormlock.backends.etcd:Etcd [etcd]',
                        'mysql = stormlock.backends.mysql:MySql [mysql]',
                        'postgresql = stormlock.backends.postgresql:Postgresql '
                        '[postgresql]',
                        'redis = stormlock.backends.redis:Redis [redis]']}

setup_kwargs = {
    'name': 'stormlock',
    'version': '0.2.0',
    'description': 'Simple distributed lock with support for multiple backends',
    'long_description': '==============\nStormlock\n==============\n\n|status| |version|\n\n.. |status| image:: https://github.com/tmccombs/stormlock/workflows/Main/badge.svg\n    :alt: Build Status\n    :target: https://github.com/tmccombs/stormlock/actions\n.. |version| image:: https://img.shields.io/pypi/v/stormlock\n    :alt: Version\n\n.. note:: Stormlock is beta quality and not ready for production use.\n\nStormlock is a simple centralized locking system primarily intended for human operators (although it may also be useful in some\nsimple scripting scenarios).\n\nThe basic idea is that you acquire a lock by running a command, which gives you a "lease id". That lease id can then be used to\nrelease the lock, or extend its duration. All locks are given a duration after which they are automatically released. The lock is\nstored in  a backend, which is generally some kind of database.\n\nThe intended use case is where you have some kind of operation which happens somewhat infrequently across a distributed system,\nand you want to ensure multiple operators don\'t perform the operation at the same time. For example, this could be used to make sure\nto prevent simultaneous attempts to apply infrastructure-as-code changes, database patches, etc. to the same system by different\noperators.\n\nThis is **not** intended as a general purpose lock. It is designed with the assumption that locks can be held for a long time without\nproblems (hours or even days), and that the TTL for the lock doesn\'t need granularity better than a second. Furthermore, the availability\nof the lock is a function of the availability of the backend it uses.\n\nConcepts\n--------\n\nresource\n    A unique resource that is protected by a lock. The resource name is used as the key for storing\n    the lock in the backend.\nprincipal\n    Who is holding the lock. When a lock is held, an identifier for the principal is stored in the \n    backend so that it is easy to see who currently has the lock.\nbackend\n    Some form of database which stores the state of the lock. Multiple backends are supported, and\n    it is possible to implement your own plugin to support additional backends.\nttl\n    Time to live. How long a lease on a lock should live before expiring. Renewing a lease sets\n    a new time to live.\nlease\n    A handle on an actively held lock. You hold the lock for a resource from the time you acquire \n    a lease to the time you release it, or the lease expires. Only one lease can exist for a \n    resource at a time.\nlease id\n    A unique, opaque identifier for a lease. This id is needed to perform operations on a lease,\n    such as releasing it and renewing it. This id helps ensure multiple leases are not held\n    for the same resource at the same time.\n\nConfiguration\n-------------\n\nBy default, `stormlock` searches for a configuration file in the following locations (in order):\n\n#. `.stormlock.cfg` in the current directory\n#. `$XDG_CONFIG_HOME/stormlock.cfg` (with a default of `XDG_CONFIG_HOME=$HOME/.config`)\n#. `$HOME/.stormlock.cfg`\n\nThe configuration file is an INI-style config file that looks like this:\n\n.. code-block:: ini\n\n    # Default section is used for default configuration for locks.\n    # If a configuration isn\'t specified in a more specific section it falls back\n    # to values in here.\n    [default]\n    # ttl is the maximum time a lock can be held without renewing\n    ttl = 1 days\n    # principal is an identifier of who is holding the lock\n    principal = me@example.com\n    # specify which backend to use\n    backend = etcd\n\n    # Specify configuration for a specific lock\n    [special]\n    ttl = 30 minutes\n    backend = redis\n\n    # Backend sections have configuration specific to the backend\n    [backend.etcd]\n    host = etcd.example.com\n\n    [backend.redis]\n    url = redis://example.com:6379\n\nUsage\n-----\n\nThe `stormlock` command can be used to operate on locks using the configuration described above.\n\nThe supported operations are:\n\nstormlock acquire [--ttl=\\ *TTL*\\ ] *RESOURCE*\n    Attempt to acquire a lease on *RESOURCE*. If successful prints the lease id. Otherwise exit\n    with an error code.\nstormlock release *RESOURCE* *LEASE_ID*\n    Release the given lease for the given resource. The lease id should be ther result of calling\n    ``stormlock acquire``.\nstormlock renew [--ttl=\\ *TTL*\\ ] *RESOURCE* *LEASE_ID*\n    Attempt to renew the given lease on the given resource. If the lease is no longer the\n    active lease for the resource, returns an error code.\nstormlock current [--id-only] *RESOURCE*\n    Retrieve information about the current lease on a resource, if any. \n\n    If a lease is active returns a line containing the principal, time the lease was created,\n    and the lase id seperated by tabs.  If ``--id-only`` is passed, only the lease id is printed.\n\n    If no lease is active an error message is printed and an error code is returned.\nstormlock is-held *RESOURCE* *LEASE_ID*\n    Test if a lease is currently active. Returns a 0 status code if it is, otherwise returns a \n    non-zero status code.\n\nA specific configuration file can be specified by either supplying a file with the ``-c`` or\n``--config`` options, or with the ``STORMLOCK_CONFIG`` environment variable.\n\nBackends\n--------\n\nThe currently supported backends are:\n\n* Etcd\n    * Renewing a lock always uses the same TTL as the original acquisition\n* Redis\n* DynamoDB\n* PostgreSQL\n\nIt\'s also possible to implement your own backend by implementing the ``stormlock.Backend`` interface and registering the class in the\n``stormlock.backends`` entry point in python.\n',
    'author': 'Thayne McCombs',
    'author_email': 'astrothayne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tmccombs/stormlock',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
