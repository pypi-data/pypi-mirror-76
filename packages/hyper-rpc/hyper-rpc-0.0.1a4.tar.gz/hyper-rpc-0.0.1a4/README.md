# hyper-rpc

[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/hyper-rpc/status.svg)](https://drone.autonomic.zone/hyperpy/hyper-rpc)

## Simple RPC with Protobuf Services

Uses [grpcio_tools](https://pypi.org/project/grpc-tools) and [purerpc](https://github.com/standy66/purerpc) under the hood.

## Install

```sh
$ pip install hyper-rpc
```

## Example

> **TLDR; See the [example](./example) directory**

Define an RPC service in a `greeter.proto`.

```protobuf
syntax = "proto3";

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
  rpc SayHelloGoodbye (HelloRequest) returns (stream HelloReply) {}
  rpc SayHelloToMany (stream HelloRequest) returns (stream HelloReply) {}
  rpc SayHelloToManyAtOnce (stream HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

Then generate the services and stubs with `hyper-rpc`.

```sh
$ pip install hyper-rpc
$ hrpc greeter.proto
```

This creates `greeter_gprc.py` (services) and `greeter_pb2.py` (stubs) files.

You can then write an async-ready server.

```python
"""Greeter server."""

from greeter_grpc import GreeterServicer
from greeter_pb2 import HelloReply, HelloRequest
from purerpc import Server


class Greeter(GreeterServicer):
    async def SayHello(self, message):
        return HelloReply(message=f"Hello {message.name}")

    async def SayHelloToMany(self, input_messages):
        async for message in input_messages:
            yield HelloReply(message=f"Hello, {message.name}")


if __name__ == "__main__":
    server = Server(50055)
    server.add_service(Greeter().service)
    server.serve(backend="trio")

```

And a client.

```python
"""Greeter client."""

import anyio
import purerpc
from greeter_grpc import GreeterStub
from greeter_pb2 import HelloReply, HelloRequest


async def gen():
    for i in range(5):
        yield HelloRequest(name=str(i))


async def main():
    async with purerpc.insecure_channel("localhost", 50055) as channel:
        stub = GreeterStub(channel)
        reply = await stub.SayHello(HelloRequest(name="World"))
        print(reply.message)

        async for reply in stub.SayHelloToMany(gen()):
            print(reply.message)


if __name__ == "__main__":
    anyio.run(main, backend="trio")
```

And run them in separate terminals to see the output.

```
$ python server.py # terminal 1
$ python client.py # terminal 2
```

Output:

```
Hello, World
Hello, 0
Hello, 1
Hello, 2
Hello, 3
Hello, 4
```

Go forth and [Remote Procedure Call](https://en.wikipedia.org/wiki/Remote_procedure_call).

![The person who invented the term RPC](https://upload.wikimedia.org/wikipedia/en/9/90/BruceJayNelson.JPG)
