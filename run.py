from appLink import app

HOST = '192.168.100.142'
#HOST = '192.168.0.4'
#HOST = '172.20.10.2'


app.run(host=HOST, port='8000', debug=True)
