
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from core.database import get_session
from models.category import Category

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/")
def create_category(category: Category, session: Session = Depends(get_session)):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@router.get("/")
def list_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()
