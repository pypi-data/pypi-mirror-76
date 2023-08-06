# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioerl', 'aioerl.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aioerl',
    'version': '0.0.20200813',
    'description': "a python library that mimics the philosophy of Erlang's processes with asyncio tasks",
    'long_description': '# aioerl\n\n[![PyPI version](https://badge.fury.io/py/aioerl.svg)](https://badge.fury.io/py/aioerl)\n\n`aioerl` is a python library that mimics the philosophy of Erlang\'s processes with asyncio tasks.\n\nImplements the following ideas:\n\n- **Each process has a mailbox**: a queue to receive messages from other processes.\n- **Message passing**: processes communicate entirely with messages (from the point of view of the developer)\n- **Supervisor/monitors**: processes can monitor other processes (when a process dies or crashes, sends a message to its supervisor with the exit reason or the exception)\n\n## Why?\n\n`asyncio` is awesome and built-in structures like `asyncio.Queue` are great for communicating between tasks but is hard to manage errors.\n\nWith `aioerl`, a process just waits for incoming messages from other processes and decides what to do for each event (see [example](##example)).\n\n## Quickstart\n\nRequirements: Python 3.7+\n\nInstallation:\n\n```bash\npip install aioerl\n```\n\n## Example\n\n```python\nfrom aioerl import receive\nfrom aioerl import reply\nfrom aioerl import send\nfrom aioerl import spawn\n\nimport asyncio\n\n\nasync def ping_pong():\n    while m := await receive(timeout=10):\n        if m.is_ok:\n            if m.body == "ping":\n                await reply("pong")\n            else:\n                raise Exception("Invalid message body")\n        elif m.is_timeout:\n            return  # terminate process\n\n\nasync def main():\n    p = await spawn(ping_pong())\n\n    await send(p, "ping")\n    print(await receive())  # Message(sender=<Proc:Task-2>, event=\'ok\', body=\'pong\')\n\n    await send(p, "pang")\n    print(await receive())  # Message(sender=<Proc:Task-2>, event=\'err\', body=Exception(\'Invalid message body\'))\n\n    await send(p, "ping")\n    print(await receive())  # Message(sender=<Proc:Task-2>, event=\'exit\', body=\'noproc\')\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n## TODO:\n\nLot of things!',
    'author': 'Jordi Masip',
    'author_email': 'jordi@masip.cat',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
