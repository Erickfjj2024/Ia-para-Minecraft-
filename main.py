from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import uuid

app = FastAPI()
TRIGGER = "!ia"

@app.get("/status")
def read_root():
    return {"status": "Servidor da IA do Minecraft Online e Rodando!"}

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Minecraft bateu na porta! Conexão aceita.")
    
    subscribe_msg = {
        "header": {
            "version": 1, 
            "requestId": str(uuid.uuid4()), 
            "messageType": "commandRequest", 
            "messagePurpose": "subscribe"
        },
        "body": {"eventName": "PlayerMessage"}
    }
    await websocket.send_json(subscribe_msg)
    print("Pedido de inscrição no chat enviado ao jogo.")
    
    try:
        while True:
            # Lemos como texto primeiro para evitar que o servidor quebre
            raw_data = await websocket.receive_text()
            print(f"Recebido do jogo: {raw_data}") # Isso vai aparecer no log do Render!
            
            # Tentamos converter para JSON de forma segura
            try:
                data = json.loads(raw_data)
            except Exception as e:
                print("Aviso: O jogo mandou algo que não é JSON puro. Ignorando...")
                continue
            
            if "body" in data and "message" in data["body"]:
                texto = data["body"]["message"]
                autor = data["body"].get("sender", "Player")

                if texto.startswith(TRIGGER):
                    pergunta = texto.replace(TRIGGER, "").strip()
                    resposta_ia = f"Ola {autor}! Entendi que voce quer saber sobre: {pergunta}"
                    
                    response_cmd = {
                        "header": {
                            "version": 1, 
                            "requestId": str(uuid.uuid4()), 
                            "messageType": "commandRequest", 
                            "messagePurpose": "commandRequest"
                        },
                        "body": {
                            "commandLine": f"tellraw @a {{\"rawtext\":[{{\"text\":\"§b[IA] §f{resposta_ia}\"}}]}}",
                            "version": 1
                        }
                    }
                    await websocket.send_json(response_cmd)
                    
    except WebSocketDisconnect:
        print("Minecraft desconectou normalmente.")
    except Exception as e:
        print(f"Erro inesperado que derrubou a conexão: {e}")
