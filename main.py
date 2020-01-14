from backend.commands import Benchmark
from configparser import ConfigParser

import json
import time


def main():
    config = ConfigParser()
    config.read("config.ini")
    hosts = json.loads(config.get("system", "hosts"))
    benchmark = Benchmark(config, hosts)
    benchmark.run_setup()
    output = benchmark.run_all()

    logfile = f"sysbench_{time.strftime('%Y%m%d-%H%M%S')}.log"
    print(f"Saving execution log to: {logfile}")
    with open(logfile, "w") as log:
        log.write(json.dumps(output, indent=4, sort_keys=True))
        log.flush()


if __name__ == "__main__":
    main()
