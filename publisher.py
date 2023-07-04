import time
import paho.mqtt.client as mqtt
import psycopg2
import random

broker_host = "localhost"
broker_port = 1883
topic = "consumo-do-poste"
username = ""
password = ""

conn = psycopg2.connect(
    host="localhost",
    database="postes",
    user="aline",
    password="aline123"
)

cursor = conn.cursor()
query_select = "SELECT id, consumo_esperado FROM postes"
cursor.execute(query_select)
dados = cursor.fetchall()

#Simulação de dados dos postes
client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker_host, broker_port)
for id_poste, consumo_esperado in dados:
    if random.random() <= 0.3:
        variacao = random.uniform(-1.0, 1.0)
    else:
        variacao = random.uniform(-0.1, 0.1)
    consumo_medido = consumo_esperado * (1 + variacao)
    mensagem = f"{id_poste},{consumo_medido}"
    client.publish(topic, mensagem)
    time.sleep(0.2)
cursor.close()
conn.close()