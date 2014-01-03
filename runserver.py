from server import app
import sys

# For uwsgi live version
app.config['siteurl'] = '/'

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ['-d', '--debug']:
        print '-' * 60
        print '\tRUNNING IN DEBUG MODE | NOT FOR LIVE SITE'
        print '-' * 60
        app.config['siteurl'] = '/'
        app.run(debug=True)
    else:
        print '\n\tLift Database'
        print '\t- LIVE MODE\n'
        app.config['siteurl'] = '/'
        app.run(debug=False, host='0.0.0.0', port=10080)
