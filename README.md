# Tips for Deploying Python Apps with uWSGI

Test source code for the blog post
[Tips for Deploying Python Apps with uWSGI]().

## Setup

Create a temporary virtualenv with

virtualenv env

Run `pip install -r requirements.txt`.

## Run

Run the test app with:

  ` ./run.sh`

and then visit in your browser:

    http://localhost:8080/

Open a second shell to run [uwsgitop](https://github.com/xrmx/uwsgitop)
(included in the `requirements.txt`),
and look at the stacktraces.
**Don't forget to activate the virtualenv** with:

    . env/bin/activate

## Signaling remote-pdb

We want to make sure that the worker you want to debug
gets the signal. To do this, we register a signal for *all* workers.
Each worker then reads a text file,
which contains the number of the problematic worker.
If a worker reads its own number, it will start the debugger,
otherwise ignore the signal.
The signal is triggered by changing the text file.
This means, to launch a remote debugger for worker `3`,
only those two steps are required:

1. To activate the remote debugger for worker 3,
   you need to write its ID in the file 'start-remote-debugger.txt,
   for example:
   `echo 3 > ./start-remote-debugger.txt`
   See the `WID` column in `uwsgitop` or the raw stats data
   if you want to find out the worker ID.
   Or use the number of the tracebacker socket.
2. Connect to the remote-PDB server using telnet:
   `telnet localhost 8002`.
   Quit the debugger with: `quit()`
