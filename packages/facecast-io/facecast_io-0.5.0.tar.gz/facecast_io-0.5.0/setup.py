# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['facecast_io', 'facecast_io.entities']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'email-validator>=1.1.1,<2.0.0',
 'httpx>=0.12.1,<0.13.0',
 'pydantic>=1.6.1,<2.0.0',
 'pyquery>=1.4.1,<2.0.0',
 'retry>=0.9.2,<0.10.0',
 'shellingham>=1.3.2,<2.0.0',
 'tld>=0.12.2,<0.13.0',
 'typer>=0.3.1,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['typing>=3.7,<4.0', 'typing_extensions>=3.7,<4.0']}

setup_kwargs = {
    'name': 'facecast-io',
    'version': '0.5.0',
    'description': 'Unofficial API for facecast.io',
    'long_description': '***********\nFacecast IO\n***********\n\nUnofficial API client to https://facecast.io service\n####################################################\n\nInstallation\n************\n\n:pip: pip install facecast-io\n:poetry: poetry add facecast-io\n\nUsage as a library\n******************\n\n::\n\n    api = FacecastAPI(os.environ["FACECAST_USERNAME"], os.environ["FACECAST_PASSWORD"])\n    # display available devices\n    print(api.devices)\n\n    # get device by name\n    d = api.devices[\'Dev name\']\n\n    # delete specific device and all devices\n    api.devices.delete_device(\'Dev name\')\n    api.devices.delete_all()\n\n    # create device\n    api.devices.create_device(\'Dev name\')\n\n    # display device server url and key\n    print(d.input_params)\n\n    # display outputs of device\n    print(d.outputs)\n\n    # create new output\n    d.create_output("Youtube", \'rtmp://a.youtube.com\', \'youtube-key\')\n\n    # start/stop output\n    d.start_outputs()\n    d.stop_outputs()\n\n    # delete all outputs\n    d.delete_outputs()\n\n\nUsage in command line mode\n**************************\nFirst of all you need to login into your Facecast.io account:\n::\n\n    $ python -m facecast_io login\n\nNow you\'re able to work with your devices. Some of useful commands.\n\nCheck all existing devices:\n::\n\n    $ python -m facecast_io devices list\n\nCreate new device\n::\n\n    $ python -m facecast_io devices create somename\n\nShow info about specific device\n::\n\n    $ python -m facecast_io device someone\n\nShow stream params for device\n::\n\n    $ python -m facecast_io device someone --input\n\nStart and stop outputs for device\n::\n\n    $ python -m facecast_io device someone --start\n    $ python -m facecast_io device someone --stop\n\nProvision data from API into Facecast. If we have pipeline that send following structure:\n::\n\n    [\n      {\n        "channel_name": "YT ALLATRA TV Italia",\n        "server_url": "url",\n        "stream_key": "key",\n      },\n    ]\n\nCall command would be next:\n::\n\n    $ http GET \'https://streams.com/some\' | jq .devname | python -m facecast_io devices provision devname\n',
    'author': 'Serhii Khalymon',
    'author_email': 'sergiykhalimon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skhalymon/facecast-io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
