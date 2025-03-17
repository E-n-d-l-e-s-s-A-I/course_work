from fastapi import FastAPI
from schemas import TaskInput
from solver import solve

app = FastAPI(
    title="SolveApi",
    version="1.0.0",
    contact={"name": "Maksim Omelchenko", "email": "omelchenko.ma@dns-shop.ru"},
)


@app.post("/solve")
def solve_task(task_input: TaskInput):
    return solve(task_input)
