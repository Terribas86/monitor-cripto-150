from flask import Flask
import threading, time, urllib.request, urllib.parse, json
app = Flask(__name__)
CARTEIRA = {"SOL": {"qtd": 0.4049462649, "investido": 41.19}, "SUI": {"qtd": 34.1179163203, "investido": 29.25}, "RENDER": {"qtd": 15.775136808, "investido": 27.90}}
TELEFONE = "554184363725"
APIKEY = "2822761"
META = 150
def te_ligar(msg):
    try:
        url = f"https://api.callmebot.com/call.php?phone={TELEFONE}&text={urllib.parse.quote(msg)}&apikey={APIKEY}&lang=pt-br-parana-nn"
        urllib.request.urlopen(url)
    except: pass
def pega_precos():
    with urllib.request.urlopen("https://api.binance.com/api/v3/ticker/price") as r:
        dados = json.loads(r.read().decode())
    return {d['symbol']: float(d['price']) for d in dados}
def monitor():
    while True:
        try:
            precos = pega_precos()
            total = sum(info['qtd'] * precos.get(f"{m}USDT",0) for m, info in CARTEIRA.items())
            lucro = total - 98.34
            if lucro >= META:
                te_ligar(f"Meta batida! Lucro de {lucro:.0f} dolares! Total {total:.0f}")
                time.sleep(86400)
            time.sleep(300)
        except: time.sleep(60)
threading.Thread(target=monitor, daemon=True).start()
@app.route('/')
def home():
    return "Monitor ativo! Te ligo quando bater 150 de lucro"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
