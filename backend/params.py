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
                "memory-total-size": "5G"
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
                "time": "10"
            }
        },
        "oltp_read_write": {
            "all": {
                "mysql-db": "sysbench_test",
                "mysql-user": "root",
                "mysql-password": "password",
            },
            "prepare": {
                "time": "60",
                "table_size": "250000000",
                "tables": "10"
            },
            "run": {
                "time": "60",
                "table_size": "250000000",
                "tables": "10",
                "max-requests": "0"
            }
        }
    }

    return mapping.get(test, {}).get(cmd, {})
