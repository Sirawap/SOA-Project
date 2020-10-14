import time
import flask # server
#import requests # client

# Preparation of Flask server (micro web framework)
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# REST endpoint: GET test1
# just returns OK
@app.route('/contac', methods=['GET'])
def test1():
    # time.sleep(5) # This is for exercise of timeouts
    return 'Test1 OK' # no response object, because this is just a test -> response is auto created

# REST endpoint: GET test2
# call test1 and just returns response from test1 and test2
@app.route('/test2', methods=['GET'])
def test2():
    response = requests.get('http://localhost:54321/test1', timeout=1) # call EP test1
    print(response.content)
    if response.ok:
        # response content is binary, str() does not: we need to decode that, make sure the content is really UTF-8
        return response.content.decode('utf-8') + ' and Test2 OK'
    else:
        return 'Test2 Error' # Also a HTTP 200 !

# Main
# Start the web server and Flask
# use port 54321
if __name__ == "__main__":
    app.run(port=54321)


