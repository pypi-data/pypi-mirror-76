"""Simple RPC with Protobuf Services."""
from argparse import ArgumentParser, FileType
from shlex import split
from subprocess import run


def main():
    """Command-line entrypoint."""
    parser = ArgumentParser(description="Generate hrpc service and stubs")
    parser.add_argument("protobuf", type=FileType("r"), help="protobuf file")
    args = parser.parse_args()
    generate(args)


def generate(args):
    """Generate services and stubs."""
    cmd = (
        "python -m grpc_tools.protoc "
        "--purerpc_out=. "
        "--python_out=. "
        "-I. "
        f"{args.protobuf.name}"
    )
    run(split(cmd))
