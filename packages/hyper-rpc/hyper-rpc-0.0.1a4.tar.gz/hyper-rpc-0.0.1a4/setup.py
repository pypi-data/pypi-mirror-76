# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyper_rpc']

package_data = \
{'': ['*']}

install_requires = \
['grpcio_tools>=1.31.0,<2.0.0', 'purerpc>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['hrpc = hyper_rpc.hrpc:main']}

setup_kwargs = {
    'name': 'hyper-rpc',
    'version': '0.0.1a4',
    'description': 'Simple RPC with Protobuf Services',
    'long_description': '# hyper-rpc\n\n[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/hyper-rpc/status.svg)](https://drone.autonomic.zone/hyperpy/hyper-rpc)\n\n## Simple RPC with Protobuf Services\n\nUses [grpcio_tools](https://pypi.org/project/grpc-tools) and [purerpc](https://github.com/standy66/purerpc) under the hood.\n\n## Install\n\n```sh\n$ pip install hyper-rpc\n```\n\n## Example\n\n> **TLDR; See the [example](./example) directory**\n\nDefine an RPC service in a `greeter.proto`.\n\n```protobuf\nsyntax = "proto3";\n\nservice Greeter {\n  rpc SayHello (HelloRequest) returns (HelloReply) {}\n  rpc SayHelloGoodbye (HelloRequest) returns (stream HelloReply) {}\n  rpc SayHelloToMany (stream HelloRequest) returns (stream HelloReply) {}\n  rpc SayHelloToManyAtOnce (stream HelloRequest) returns (HelloReply) {}\n}\n\nmessage HelloRequest {\n  string name = 1;\n}\n\nmessage HelloReply {\n  string message = 1;\n}\n```\n\nThen generate the services and stubs with `hyper-rpc`.\n\n```sh\n$ pip install hyper-rpc\n$ hrpc greeter.proto\n```\n\nThis creates `greeter_gprc.py` (services) and `greeter_pb2.py` (stubs) files.\n\nYou can then write an async-ready server.\n\n```python\n"""Greeter server."""\n\nfrom greeter_grpc import GreeterServicer\nfrom greeter_pb2 import HelloReply, HelloRequest\nfrom purerpc import Server\n\n\nclass Greeter(GreeterServicer):\n    async def SayHello(self, message):\n        return HelloReply(message=f"Hello {message.name}")\n\n    async def SayHelloToMany(self, input_messages):\n        async for message in input_messages:\n            yield HelloReply(message=f"Hello, {message.name}")\n\n\nif __name__ == "__main__":\n    server = Server(50055)\n    server.add_service(Greeter().service)\n    server.serve(backend="trio")\n\n```\n\nAnd a client.\n\n```python\n"""Greeter client."""\n\nimport anyio\nimport purerpc\nfrom greeter_grpc import GreeterStub\nfrom greeter_pb2 import HelloReply, HelloRequest\n\n\nasync def gen():\n    for i in range(5):\n        yield HelloRequest(name=str(i))\n\n\nasync def main():\n    async with purerpc.insecure_channel("localhost", 50055) as channel:\n        stub = GreeterStub(channel)\n        reply = await stub.SayHello(HelloRequest(name="World"))\n        print(reply.message)\n\n        async for reply in stub.SayHelloToMany(gen()):\n            print(reply.message)\n\n\nif __name__ == "__main__":\n    anyio.run(main, backend="trio")\n```\n\nAnd run them in separate terminals to see the output.\n\n```\n$ python server.py # terminal 1\n$ python client.py # terminal 2\n```\n\nOutput:\n\n```\nHello, World\nHello, 0\nHello, 1\nHello, 2\nHello, 3\nHello, 4\n```\n\nGo forth and [Remote Procedure Call](https://en.wikipedia.org/wiki/Remote_procedure_call).\n\n![The person who invented the term RPC](https://upload.wikimedia.org/wikipedia/en/9/90/BruceJayNelson.JPG)\n',
    'author': 'decentral1se',
    'author_email': 'hi@decentral1.se',
    'maintainer': 'decentral1se',
    'maintainer_email': 'hi@decentral1.se',
    'url': 'https://github.com/hyperpy/hyper-rpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
