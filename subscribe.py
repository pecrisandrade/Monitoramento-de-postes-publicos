import paho.mqtt.client as mqtt
import psycopg2
import random

broker_host = "localhost"
broker_port = 1883
topic = "consumo-do-poste"
username = ""
password = ""

#Conexão com o DB
conn = psycopg2.connect(
    host="localhost",
    database="postes",
    user="aline",
    password="aline123"
)

cursor = conn.cursor() #Iniciar cursor

# Decodificação das informações da tabela
def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    id_poste, consumo_medido = mensagem.split(",")
    query_select = "SELECT id FROM postes WHERE id = %s"
    cursor.execute(query_select, (id_poste,))
    existing_record = cursor.fetchone()
    
    #Query de seleção
    query_select = "SELECT consumo_esperado FROM postes WHERE id = %s"
    cursor.execute(query_select, (id_poste,))
    consumo_esperado = cursor.fetchone()[0]
    percentual_variacao = (float(consumo_medido) - consumo_esperado) / consumo_esperado * 100

    #Alertas
    if percentual_variacao > 50:
        alerta = "Possivel roubo de energia"
    elif -100 <= percentual_variacao < -50:
        alerta = "Lâmpada possivelmente queimada"
    else:
        alerta = None
    
    #Update ou inserção
    if existing_record:
        query_update = "UPDATE postes SET consumo_medido = %s, alerta = %s, percentual_variacao = %s WHERE id = %s"
        values_update = (consumo_medido, alerta, percentual_variacao, id_poste)
        cursor.execute(query_update, values_update)
        print(f"Registro com ID {id_poste} atualizado com sucesso. Consumo medido: {consumo_medido}")
    else:
        query_insert = "INSERT INTO postes (id, consumo_esperado, consumo_medido, alerta, percentual_variacao) VALUES (%s, %s, %s, %s, %s)"
        values_insert = (id_poste, consumo_esperado, consumo_medido, alerta, percentual_variacao)
        cursor.execute(query_insert, values_insert)
        print(f"Novo registro com ID {id_poste} inserido com sucesso. Consumo medido: {consumo_medido}")
    
    conn.commit()

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_message = on_message
client.connect(broker_host, broker_port)
client.subscribe(topic)
client.loop_forever()