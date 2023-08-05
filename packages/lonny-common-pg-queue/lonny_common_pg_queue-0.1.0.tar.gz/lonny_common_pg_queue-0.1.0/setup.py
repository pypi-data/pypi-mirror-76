# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonny_common_pg_queue']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lonny-common-pg-queue',
    'version': '0.1.0',
    'description': 'A lightweight distributed queue using a postgres DB.',
    'long_description': '# `lonny_pg_queue`\n\nA lightweight distributed queue using a postgres DB.\n\n## Installation\n\n```bash\npip install lonny_pg_queue\n```\n\n## Usage\n\nThe first step is importing the `Queue` class. This can be done as:\n\n```python\nfrom lonny_pg_queue import Queue\n```\n\nWe then need to ensure the requisite queue table is implemented. This can be done by passing a `lonny_db` connection object to the `Queue.setup(db)` method (This method is idempotent and can be run multiple times).\n\nTo create a `queue` object simply invoke the constructor with a `lonny_db` connection and a mandatory `namespace`:\n\n```python\nqueue_1 = Queue(db, "queue_1")\nqueue_2 = Queue(db, "queue_2")\n```\n\nThe messages placed in these queues will be isolated from one another.\n\nTo enqueue objects, simply call `queue.put(obj)` on any JSON serializable object.\n\nTo retrieve an object from the queue, call `queue.get()`. This will return a `Message` object. The underlying payload can be accessed via `message.payload`. Messages work similar to how they work in AWS SQS - messages retrieved from the queue are immediately "locked". In this state they cannot be retrieved by another consume. After a timeout, they become unlocked and can be accessed as before by another consumer. This happens a maximum number of times until the message is deleted permanently. \n\nOnce you are done with a message, you should call `.consume()` on it - this will prevent it being accessed again at a later point. To simplify this procedure, we can use the `with` syntax:\n\n```python\nwith queue.get() as payload:\n    do_stuff(payload)\n```\n\nIf we leave the block with no exception, the message is consumed/deleted as expected. However, if something goes wrong, `consume` isn\'t called, giving us another chance in the future to handle this message.\n\n',
    'author': 'tlonny',
    'author_email': 't@lonny.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lonny.io',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
