from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Servidor Online!"}

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    # Apenas aceita a conexão, sem enviar o pedido de "subscribe" ainda
    await websocket.accept()
    print(">>> MINECRAFT CONECTOU COM SUCESSO! <<<")
    
    try:
        while True:
            # Fica aguardando qualquer sinal de vida do jogo
            data = await websocket.receive_text()
            print(f"O jogo enviou: {data}")
            
    except WebSocketDisconnect as e:
        print(f">>> O JOGO DESCONECTOU! Código do erro: {e.code} <<<")
    except Exception as e:
        print(f">>> ERRO NO PYTHON: {e} <<<")
