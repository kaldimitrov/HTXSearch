from flask import Flask, request
import json
 
app = Flask(__name__)

def process(query):
  return { "response": query }

@app.route('/submit', methods=['POST'])
def submit():
  if request.method != 'POST':
    return
  data = json.loads(request.data.decode())
  return process(data['query'])
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)