#!/usr/bin/python3
from flask import Flask,jsonify,render_template
from app import monitor
from config.settings import SERVER_HOST,SERVER_PORT

app=Flask(__name__)

@app.route('/api/data')
def api_data():
    #取得数据
    data=monitor.collect_system_data()
    #保存数据
    monitor.save_to_db(data)
    #返回数据
    return jsonify(data)

@app.route('/')
def index():
    data=monitor.collect_system_data()
    monitor.save_to_db(data)
    return render_template('index.html',data=data)
    
def start_server():
    print(f"🔥 ServerMonitor 启动中...http://{SERVER_HOST}:{SERVER_PORT}")
    app.run(host=SERVER_HOST,port=SERVER_PORT,debug=False)

if __name__=='__main__':
    start_server()




