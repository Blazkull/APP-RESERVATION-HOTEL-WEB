from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from core.database import get_session
from models.user import User
from sqlmodel import select

templates = Jinja2Templates(directory="templates")

@app.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.username == username)).first()

    if not user or user.password != password:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Usuario o contraseña incorrectos"
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": f"Bienvenido, {user.fullname or user.username}!"
    })
