from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template,stream_with_context
from gevent.pywsgi import WSGIServer
import json
import time
import mysql.connector
#import MySQLdb

app = Flask(__name__)
counter = 0

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mypot"
)
##############################
@app.route("/")
def render_index():
  return render_template("index.html")

##############################
##############################

def getDB(data):
  data_list = data.split(", ")
  insertrec = db.cursor()
  sqlqurey="insert into honeypot(type,alert,date,time,ip_attacker,ip_server,protocol,comment) values ('"+data_list[0]+"','"+data_list[1]+"','"+data_list[2]+"','"+data_list[3]+"','"+data_list[4]+"','"+"-"+"','"+data_list[5]+"','"+data_list[6]+"')"
  insertrec.execute(sqlqurey)
  print("commit")
  db.commit()
  #db.close()

##############################
@app.route("/listen")
def listen():

  def respond_to_client():
    while True:
      global counter
      #log_lines = []
      with open("DBcowrie.txt", "r+") as f:
        for line in f.readlines():
          getDB(line)
          print(line)
          print("******************")
          print(counter)
          counter += 1
          _data = json.dumps({"line":line, "counter":counter})
          yield f"id: 1\ndata: {_data}\nevent: online\n\n"
      with open("DBcowrie.txt", "w+") as f:
        f.write("")
      time.sleep(0.5)
  return Response(respond_to_client(), mimetype='text/event-stream')

##############################

if __name__ == "__main__":
  app.run(host="192.168.1.111", port=50100, debug=True)
  http_server = WSGIServer(("192.168.1.111", 50100), app)
  http_server.serve_forever()








