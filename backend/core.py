from __future__ import print_function
from pssh.clients import ParallelSSHClient
from pssh.exceptions import UnknownHostException
from .params import get_params

import json


class SessionRunner:

    def __init__(self, config, hosts):
        self.config = config
        self.hosts = json.loads(self.config.get("system", "hosts"))
        if isinstance(self.hosts, dict):
            self.host_config = self.hosts
            self.hosts = self.hosts.keys()
        self.output = None
        self.prepare_fileio = True
        self.test_type = None

    def connect_ssh(self, retries=6, user="root"):
        kwargs = {"num_retries": retries}
        if hasattr(self, "host_config"):
            kwargs["host_config"] = self.host_config
        else:
            kwargs["user"] = user
        self.client = ParallelSSHClient(self.hosts, **kwargs)

    def run_command(self):
        if not hasattr(self, "client"):
            self.connect_ssh()

        if hasattr(self, "command"):
            try:
                self.output = self.client.run_command(self.command)
            except UnknownHostException as e:
                print(f"Unknown Host {e.host} - {e.args[2]}")
            except Exception as e:
                print(e)

        return self.get_output()

    def get_output(self):
        command_output = {}
        if self.output:
            for host, host_output in self.output.items():
                command_output[host] = {
                    "command": self.command,
                    "stdout": list(host_output.stdout),
                    "stderr": "\n".join(list(host_output.stderr)),
                    "exit_code": host_output.exit_code
                }

        return command_output

    def make_command(self, *args, cmd="run", threads=None):
        threads = f"--threads={threads or '$(nproc)'}"
        args = list(args)
        args.extend(get_params(self.config, self.test_type, cmd))
        self.command = " ".join(["sysbench", self.test_type, *args,
                                 threads, cmd])