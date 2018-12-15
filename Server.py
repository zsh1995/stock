from flask import Flask, jsonify, Response,render_template
import json

import macd_calc
import price_calc
import rsi_calc
import numpy as py
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('rsi.html')

@app.route("/price/index")
def priceindex():
    return render_template('price.html')

@app.route('/macd')
def macdval():
    macd, macdsign, macdhist, date = macd_calc.calc_macd()
    data = {
         "macd": macd.tolist(),
         "macdsign": macdsign.tolist(),
         "macdhist": macdhist.tolist(),
         "date": date.tolist()
     }
    jsonfy = json.dumps(data)
    res = Response(jsonfy, mimetype='application/json')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route("/macd/index")
def macdindex():
    return render_template('macd.html')





@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/rsi_state')
def rsi_state():
    nw = rsi_calc.calc_rsi()
    state_list =[]
    rsi_calc.rsi_local_max_all(nw, state_list)
    rsi_calc.short_uncross_long(nw, state_list)
    rsi_calc.loca_max_term(nw, state_list)
    rsi_calc.rsi_back_calc(rsi_calc.get_histroy_price()["close"], nw, state_list)
    group_data = {
        "rsi_data":{
            "rsi1" : nw['rsi6'],
            "rsi2": nw['rsi12'],
            "rsi3": nw['rsi24'],
            "date": nw['date']
        },
        "rsi_state":state_list,
    }
    jsonfy = json.dumps(group_data, default=lambda obj: obj.__dict__)
    res =  Response(jsonfy, mimetype='application/json')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
@app.route('/price/<freq>')
def date_price(freq):
    history = price_calc.loal_data(freq)
    data = {
        "price": {
            "open": history["open"].tolist(),
            "close": history["close"].tolist(),
            "high": history['high'].tolist(),
            "low": history['low'].tolist()
        },
        "date": history["trade_date"].tolist()

    }
    jsonfy = json.dumps(data, default=lambda obj: obj.__dict__)
    res = Response(jsonfy, mimetype='application/json')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/price/shake/<term>/<freq>')
def price_shake(term, freq):
    if term == None:
        shake_states = price_calc.calc_shake(freq = freq)
    else:
        shake_states =price_calc.calc_shake(int(term), freq = freq)
    data =  shake_states
    jsonfy = json.dumps(data, default=lambda obj: obj.__dict__)
    res = Response(jsonfy, mimetype='application/json')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)