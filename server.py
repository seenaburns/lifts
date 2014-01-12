from flask import Flask, request, Response, g, render_template
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
    logs = g.db.logs(10000)
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

@app.route('/graph/<liftname>/<reps>/')
def graph(liftname, reps):
    # Get logs
    logs = g.db.search(liftname)
    
    # Create (date, weight) tuples
    data = []
    for l in logs:
        # Remove reps, remove failed tag
        sets = [x.split('x')[0].split('-')[0] for x in g.db.get_sets(l)]
        date = g.db.get_date(l)
        for x in sets:
            data.append((date, x))
    print data
    
    # Format data for js
    js_data = ', '.join(['["%s", %s]' % (x[0], x[1]) for x in data])
    #sets = [(g.db.get_date(x), g.db.get_sets(x)) for x in logs]
    #set_weights = [[y.split('x')[0].split('-')[0] for y in x] for x in sets]
    #set_weights = [(weight, 20) for subl in set_weights for weight in subl]
    #format_weights = ', '.join(['[%s, %s]' % (x[0], x[1]) for x in set_weights])
    #print set_weights
    return render_template('graph.html', data=js_data)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ['-d', '--debug']:
        # Debug version
        print 'Debug'
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=10081)
