import random
import time
import uwsgi

from flask import Flask
from remote_pdb import RemotePdb

remote_pdb_port = 8002
remote_pdb_filename = "./start-remote-debugger.txt"

app = Flask(__name__)


def wait1(secs):
    time.sleep(secs)


def wait2(secs):
    wait1(secs)


def wait3(secs):
    wait2(secs)


def wait4(secs):
    wait3(secs)


def wait5(secs):
    wait4(secs)


@app.route('/wait/<int:secs>')
def wait_secs(secs):
    wait5(secs)
    return 'Waited {} seconds. <a href="/">Back</a>'.format(secs)


@app.route('/wait/random')
def wait_random():
    secs = random.randint(0, 7)
    wait5(secs)
    return 'Waited {} seconds. <a href="/">Back</a>'.format(secs)


@app.route('/')
def index():
    return """
    Hello!

    <p><a href="wait/random">Wait a few seconds</a>
       -&gt; blocks for a few seconds,
       so that <b>uwsgitop</b> shows interesting stats.
       <pre>uwsgitop localhost:8001</pre></p>
    <p><a href="wait/60">Wait 60 seconds</a>
       -&gt; waits long enough so you can print the stack traces of all workers with
       <pre>./print-stack-traces.sh</pre>
       uwsgitop should show a blocked worker.</p>
    <p><a href="wait/90">Wait 90 seconds</a>
       -&gt; triggering <b>harakiri</b> after 65s</p>
    <hr>
    <p>Write the number of a worker process into {rpdb_filename}
       to enable remote_pdb on port {rpdb_port}.
       <pre>echo 3 > {rpdb_filename}</pre>
    Then, access the remote debugger:
    <pre>telnet localhost 8002</pre>
    </p>
    """.format(rpdb_filename=remote_pdb_filename, rpdb_port=remote_pdb_port)


def start_remote_debugger_if_correct_worker(*arg):
    with open(remote_pdb_filename) as f:
        wanted_worker = f.read().strip()
        this_worker = str(uwsgi.worker_id())

        if wanted_worker != this_worker:
            print("This worker is {}, not {}".format(this_worker, wanted_worker))
            return

    print("I'm worker {}! Starting remote PDB server on port {}.".format(
        this_worker, remote_pdb_port))
    return RemotePdb('127.0.0.1', remote_pdb_port).set_trace()


def signal_all_workers_to_run_function_on_file_change(filename, func):
    uwsgi.register_signal(30, 'workers', func)
    uwsgi.add_file_monitor(30, filename)


signal_all_workers_to_run_function_on_file_change(
    remote_pdb_filename, start_remote_debugger_if_correct_worker)
