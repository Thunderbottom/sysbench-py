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

    mysql_user = config.get("/usr/share/doc/sysbench/tests/db/oltp.lua",
                            "mysql-user")
    mysql_password = config.get("/usr/share/doc/sysbench/tests/db/oltp.lua",
                                "mysql-password")
    cmd = "select table_schema, round(sum(data_length + index_length)/1024/1024/1024, 1) from information_schema.tables group by table_schema"
    db_size_cmd = f"mysql -u {mysql_user} -p{mysql_password} -e {cmd}"
    output["database"] = benchmark.make_command(db_size_cmd, run=True)

    logfile = f"sysbench_{time.strftime('%Y%m%d-%H%M%S')}.log"
    print(f"Saving execution log to: {logfile}")
    with open(logfile, "w") as log:
        log.write(json.dumps(output, indent=4, sort_keys=True))
        log.flush()


if __name__ == "__main__":
    main()
