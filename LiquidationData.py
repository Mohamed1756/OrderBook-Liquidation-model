import asyncio
import json
import os
from websockets import connect
from datetime import datetime, timezone

websocket_uri = "wss://fstream.binance.com/ws/!forceOrder@arr"
filename = "binance.csv"

if not os.path.isfile(filename):
    with open(filename, "w") as f:
        f.write(",".join(["Symbol", "Side", "Order Type", "Original Quantity",
                          "Liq Price", "Order Status", "TimeStamp", "Value"]) + "\n")


async def binance_liquidations(uri, filename):
    async for websocket in connect(uri):
        try:
            while True:
                msg = await websocket.recv()
                print(msg)
                msg = json.loads(msg)["o"]
                symbol = msg["s"]
                side = msg["S"]
                order_type = msg["o"]
                quantity = float(msg["q"])

                average_price = float(msg["ap"])
                order_status = msg["X"]
                timestamp = int(msg["T"])
                value = quantity * average_price

                # Convert timestamp to UTC datetime
                trade_time = datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc).strftime('%H:%M:%S')

                data = [symbol, side, order_type, str(quantity),str(average_price), order_status,
                        trade_time, str(value)]

                with open(filename, "a") as f:
                    f.write(",".join(data) + "\n")
        except Exception as e:
            print(e)
            continue


asyncio.run(binance_liquidations(websocket_uri, filename))
