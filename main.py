from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from database import Deposit, SessionLocal, engine
import logging


logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/")
async def calculate_deposit(request: Request, amount: float = Form(...), rate: float = Form(...)):
    deposit = amount * (1 + rate / 100) ** 12
    db = SessionLocal()
    new_deposit = Deposit(amount=amount, rate=rate, deposit=deposit)
    db.add(new_deposit)
    db.commit()
    db.close()
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.get("/home")
def read_home(request: Request):
    db = SessionLocal()
    deposits = db.query(Deposit).all()
    db.close()
    deposits_list = [{"amount": deposit.amount, "rate": deposit.rate, "deposit": deposit.deposit} for deposit in deposits]
    return templates.TemplateResponse("home.html", {"request": request, "deposits": deposits_list})
