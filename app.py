import random
import time
import os
from pycoingecko import CoinGeckoAPI
from paho.mqtt import client as mqtt_client

broker = os.getenv('BROKER')
port = int(os.getenv('BROKER_PORT', 1883))
username = os.getenv('BROKER_USERNAME','')
password = os.getenv('BROKER_PASSWORD','')
topic = os.getenv('TOPIC', 'coingecko2mqtt')
sleep_time = int(os.getenv('SLEEP_TIME', 30))
MQTT_CLIENT_ID = "coingecko2mqtt"

CoinGeckoKey = os.getenv('COINGECKO_KEY', '')

Corrency = os.getenv('CORRENCY', 'usd')

coins = os.getenv('COIN', 'bitcoin').split(',')

firstrun = True

if CoinGeckoKey:
    cg = CoinGeckoAPI(demo_api_key=CoinGeckoKey)
else:
    cg = CoinGeckoAPI()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(MQTT_CLIENT_ID)
    if username and password:
        client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def get_prices(coins):
    data = cg.get_price(ids=','.join(coins), vs_currencies=Corrency, include_24hr_change='true')
    return data

def publish(client):
    global firstrun
    while True:
        if not firstrun == True:
            time.sleep(sleep_time)
        prices = get_prices(coins)
        for coin in coins:
            if coin not in prices:
                continue
            price = prices[coin][Corrency]
            change24h = prices[coin][f'{Corrency}_24h_change']
            publish_topic = topic + "/" + coin
            msg = f"{price} , 24h change: {change24h}"
            result_price = client.publish(publish_topic + "/price", price)
            result_24h_change = client.publish(publish_topic + "/24h_change", change24h)
            status_price = result_price.rc
            status_24h_change = result_24h_change.rc
            if status_price == 0 and status_24h_change == 0:
                print(f"Send `{msg}` to topic `{publish_topic}`")
            else:
                print(f"Failed to send message to topic {publish_topic}")
        firstrun = False


def run():
    global firstrun
    client = connect_mqtt()
    client.loop_start()
    firstrun = True
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()