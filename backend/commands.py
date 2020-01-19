from .core import SessionRunner


class Benchmark(SessionRunner):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cpu_benchmark(self):
        self.test_type = "cpu"
        self.make_command()

    def memory_benchmark(self):
        self.test_type = "memory"
        self.make_command()

    def fileio_benchmark(self, cleanup=False):
        self.test_type = "fileio"

        if cleanup:
            self.prepare_fileio = True
            self.make_command(cmd="cleanup")
            return

        if self.prepare_fileio:
            self.prepare_fileio = False
            self.make_command(cmd="prepare")
            self.run_command()

        self.make_command()

    def thread_benchmark(self, threads=128, timeout=10):
        self.test_type = "threads"
        self.make_command(threads=threads)

    def oltp_benchmark(self, cleanup=False):
        self.test_type = "/usr/share/doc/sysbench/tests/db/oltp.lua"

        if cleanup:
            self.make_command(cmd="cleanup")

        self.make_command(cmd="prepare")
        # run oltp benchmark
        self.make_command()

    def run_all(self, iterations=1, cleanup=True):
        benchmarks = ["cpu", "memory", "fileio", "thread", "oltp"]
        out = {}
        for i in range(iterations):
            out[i + 1] = {}
            for benchmark in benchmarks:
                print(f"Running {benchmark} benchmark ({i + 1}/{iterations})")
                getattr(self, f"{benchmark}_benchmark")()
                out[i + 1][benchmark] = self.output

        if cleanup:
            self.fileio_benchmark(cleanup=True)
            self.oltp_benchmark(cleanup=True)

        return out

    def run_setup(self):
        mysql_cmd = f"CREATE DATABASE {self.config.get('/usr/share/doc/sysbench/tests/db/oltp.lua', 'mysql-db')}"
        mysql_user = self.config.get("/usr/share/doc/sysbench/tests/db/oltp.lua", "mysql-user")
        mysql_pass = self.config.get("/usr/share/doc/sysbench/tests/db/oltp.lua", "mysql-password")
        self.command = f"mysql -u {mysql_user} -p{mysql_pass} -e {mysql_cmd}"
        self.run_command()
