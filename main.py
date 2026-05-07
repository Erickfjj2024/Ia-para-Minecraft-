from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# Rota HTTP isolada para o UptimeRobot não deixar o servidor dormir
@app.get("/status")
def read_status():
    return {"status": "Servidor Online!"}

# Rota WebSocket isolada APENAS para o Minecraft
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # O Bedrock às vezes exige o protocolo dele, mas vamos tentar aceitar tudo primeiro
    await websocket.accept()
    print(">>> MINECRAFT CONECTOU COM SUCESSO! <<<")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"O jogo enviou: {data}")
            
    except WebSocketDisconnect as e:
        print(f">>> O JOGO DESCONECTOU! Código: {e.code} <<<")
    except Exception as e:
        print(f">>> ERRO NO PYTHON: {e} <<<")
