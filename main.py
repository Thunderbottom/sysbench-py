from backend.commands import Benchmark
from configparser import ConfigParser

import json


def main():
    config = ConfigParser()
    config.read("config.ini")
    hosts = json.loads(config.get("system", "hosts"))
    benchmark = Benchmark(config, hosts)
    benchmark.run_all()


if __name__ == "__main__":
    main()
