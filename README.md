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

1. To activate the remote debugger for a worker,
   you need to write its ID in the file 'start-remote-debugger.txt,
   for example:
   `echo 3 > ./start-remote-debugger.txt`
   See the `WID` column in `uwsgitop`.
2. Connect to the remote-PDB server using telnet:
   `telnet localhost 8002`.
   Quit the debugger with: `quit()`
