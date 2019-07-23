from io import StringIO
from mcwho.find import check_mcwho
from flask import Flask, jsonify, Response, stream_with_context, render_template, request
import json
app = Flask(__name__)

@app.route('/api/search')
def api_search():    
    search_string = request.args.get("q")
    return jsonify(list(check_mcwho(search_string)))

@app.route("/search")
def search():
    search_string = request.args.get("q")
    def generate():
        output_stream = ReadWriteStream()        
        for result in check_mcwho(search_string, output_stream):
            output = output_stream.read()
            if output: yield output.replace('\n', '<br/>')
            yield render_template("actor.html", actor=result)
    return Response(stream_with_context(generate()))

@app.route('/')
def home():
    return "Coming soon.."

class ReadWriteStream:
    def __init__(self, s=""):
        self.buffer = s

    def read(self, n=-1):
        chunk = self.buffer[:n]
        self.buffer = self.buffer[n:]
        return chunk

    def write(self, s):
        self.buffer += s