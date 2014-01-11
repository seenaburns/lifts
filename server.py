from flask import Flask, request, Response, g
import sys
import database

DATAFILE = 'data/lifts.db'

app = Flask(__name__)
# app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = database.DB_Manager(DATAFILE)
    g.db.connect()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_logs():
    logs = g.db.logs(50)
    output = ''.join(logs)
    return Response(output, mimetype='text/plain')

@app.route('/<liftname>/')
def search(liftname):
    # Get logs
    logs = g.db.search(liftname)
    output = ''.join(logs)

    # Handle zero results
    if len(logs) == 0:
        output = "No results found for '%s'" % (liftname)
    return Response(output, mimetype='text/plain')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ['-d', '--debug']:
        # Debug version
        print 'Debug'
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=10081)
