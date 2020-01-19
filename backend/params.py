def get_params(config, test_type="cpu", cmd="run"):
    params = []
    for cmd in (cmd, "all"):
        params_dict = get_params_mapping(test=test_type, cmd=cmd)
        for param in params_dict.keys():
            params.append("--{param}={value}".format(
                param=param,
                value=config.get(test_type, param,
                                 fallback=params_dict.get(param))))
    return params


def get_params_mapping(test="cpu", cmd="all"):
    mapping = {
        "cpu": {
            "all": {
                "cpu-max-prime": "20000"
            }
        },
        "memory": {
            "all": {
                "memory-block-size": "1K",
                "memory-total-size": "64G"
            }
        },
        "fileio": {
            "all": {
                "file-test-mode": "rndrw",
                "file-total-size": "15G"
            }
        },
        "threads": {
            "all": {
                "max-time": "10"
            }
        },
        "/usr/share/doc/sysbench/tests/db/oltp.lua": {
            "all": {
                "mysql-db": "sysbench_test",
                "mysql-user": "root",
                "mysql-password": "password",
            },
            "prepare": {
                "max-time": "60",
                "oltp-table-size": "25000",
                "oltp-tables-count": "100"
            },
            "run": {
                "max-time": "60",
                "oltp-table-size": "25000",
                "oltp-tables-count": "100",
                "max-requests": "0"
            }
        }
    }

    return mapping.get(test, {}).get(cmd, {})
