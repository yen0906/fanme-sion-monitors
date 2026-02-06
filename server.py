from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests, time
from threading import Thread
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
CORS(app)

URL = "https://www.kmonstar.com.tw/products/%E6%87%89%E5%8B%9F-260221-lngshot-debut-ep-shot-callers-%E5%9C%98%E9%AB%94%E6%8B%8D%E7%AB%8B%E5%BE%97%E5%90%88%E7%85%A7%E6%B4%BB%E5%8B%95-in-taipei"

last_qty = None
records = []  # 儲存差值紀錄


def fetch_qty():
    api_url = "https://www.kmonstar.com.tw/products/%E6%87%89%E5%8B%9F-260221-lngshot-debut-ep-shot-callers-%E5%9C%98%E9%AB%94%E6%8B%8D%E7%AB%8B%E5%BE%97%E5%90%88%E7%85%A7%E6%B4%BB%E5%8B%95-in-taipei"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    res = requests.get(api_url, headers=headers, timeout=10)
    res.raise_for_status()
    data = res.json()

    return int(data["total_sold"])

def monitor():
    global last_qty
    while True:
        try:
            current = fetch_qty()
            if last_qty is None:
                last_qty = current
            else:
                diff = last_qty - current
                if diff > 0:
                    taipei_time = datetime.now(
                        timezone(timedelta(hours=8))
                    ).strftime("%Y-%m-%d %H:%M:%S")

                    records.append({
                        "time": taipei_time,
                        "diff": diff
                    })

                    # 排序：減少數量大的排前面
                    records.sort(key=lambda x: x["diff"], reverse=True)

                    # 只保留前 45 名
                    records[:] = records[:45]

                    last_qty = current
        except Exception as e:
            print("error:", e)

        time.sleep(5)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def api_data():
    return jsonify(records)


if __name__ == "__main__":
    Thread(target=monitor, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)



