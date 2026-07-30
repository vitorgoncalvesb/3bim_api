from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="API de Tarefas",
    description="Uma API simples feita com FastAPI",
    version="1.0.0"
)

class Tarefa(BaseModel):
    titulo: str
    descricao: str
    concluida: bool = False

tarefas = []

@app.get("/")
def inicio():
    return {
        "mensagem": "Bem-vindo à API de Tarefas 🚀",
        "docs": "/docs"
    }

@app.get("/tarefas", response_model=List[Tarefa])
def listar_tarefas():
    return tarefas

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa):
    tarefas.append(tarefa)
    return {
        "mensagem": "Tarefa criada com sucesso!",
        "tarefa": tarefa
    }

@app.get("/tarefas/{id}")
def buscar_tarefa(id: int):
    if id >= len(tarefas):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefas[id]

@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, tarefa: Tarefa):
    if id >= len(tarefas):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefas[id] = tarefa
    return {
        "mensagem": "Tarefa atualizada!",
        "tarefa": tarefa
    }

@app.delete("/tarefas/{id}")
def remover_tarefa(id: int):
    if id >= len(tarefas):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    removida = tarefas.pop(id)
    return {
        "mensagem": "Tarefa removida!",
        "tarefa": removida
    }