from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import uuid

app = FastAPI()
TRIGGER = "!ia"

# Rota HTTP para o UptimeRobot manter o servidor vivo
@app.get("/")
def read_root():
    return {"status": "Servidor da IA do Minecraft Online e Rodando!"}

# Rota WebSocket para o Minecraft se conectar
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Minecraft conectado!")
    
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
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if "body" in data and "message" in data["body"]:
                texto = data["body"]["message"]
                autor = data["body"].get("sender", "Player")

                if texto.startswith(TRIGGER):
                    pergunta = texto.replace(TRIGGER, "").strip()
                    
                    # Aqui entra a lógica da sua API (Gemini/Groq)
                    resposta_ia = f"Ola {autor}! Entendi que voce quer saber sobre: {pergunta}"
                    
                    response_cmd = {
                        "header": {
                            "version": 1, 
                            "requestId": str(uuid.uuid4()), 
                            "messageType": "commandRequest", 
                            "messagePurpose": "commandRequest"
                        },
                        "body": {
                            # Usamos tellraw para ficar formatado bonitinho no chat
                            "commandLine": f"tellraw @a {{\"rawtext\":[{{\"text\":\"§b[IA] §f{resposta_ia}\"}}]}}",
                            "version": 1
                        }
                    }
                    await websocket.send_json(response_cmd)
                    
    except WebSocketDisconnect:
        print("Minecraft desconectado")
