from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, extract
from datetime import datetime
from decimal import Decimal
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

from core.database import SessionDep
from models.reservation import Reservation
from models.client import Client
from models.room import Room

router = APIRouter()

@router.get("/api/dashboard", tags=["DASHBOARD"],dependencies=[(Depends(decode_token))])
def get_dashboard_data(
    session: SessionDep,
    month: int = Query(default=datetime.now().month, ge=1, le=12),
    year: int = Query(default=datetime.now().year)
):
    # Total Recaudado
    total_recaudo = session.query(func.sum(Reservation.total))\
        .filter(extract('month', Reservation.check_in_date) == month)\
        .filter(extract('year', Reservation.check_in_date) == year)\
        .scalar() or Decimal(0.00)

    # Total de Habitaciones
    total_habitaciones = session.query(func.count(Room.id)).scalar() or 1  # evitar división por cero

    # Habitaciones reservadas en el mes
    habitaciones_reservadas = session.query(func.count(Reservation.id))\
        .filter(extract('month', Reservation.check_in_date) == month)\
        .filter(extract('year', Reservation.check_in_date) == year)\
        .scalar() or 0

    # Porcentaje de ocupación
    porcentaje_ocupacion = (habitaciones_reservadas / total_habitaciones) * 100

    # Promedio de días reservados
    promedio_dias = session.query(
        func.avg(func.datediff(Reservation.check_out_date, Reservation.check_in_date))
    )\
        .filter(extract('month', Reservation.check_in_date) == month)\
        .filter(extract('year', Reservation.check_in_date) == year)\
        .scalar() or 0

    # Total de clientes en el mes
    total_clientes = session.query(func.count(func.distinct(Reservation.client_id)))\
        .filter(extract('month', Reservation.check_in_date) == month)\
        .filter(extract('year', Reservation.check_in_date) == year)\
        .scalar() or 0

    return {
        "total_recaudo": float(total_recaudo),
        "porcentaje_ocupacion": round(porcentaje_ocupacion, 2),
        "promedio_dias": round(promedio_dias, 2),
        "total_clientes": total_clientes
    }

@router.get("/api/dashboard/pdf", tags=["DASHBOARD"],dependencies=[(Depends(decode_token))])
def generate_dashboard_pdf(
    session: SessionDep,
    month: int = Query(default=datetime.now().month, ge=1, le=12),
    year: int = Query(default=datetime.now().year)
):
    dashboard = get_dashboard_data(session, month, year)

    filename = f"dashboard_report_{month}_{year}.pdf"
    filepath = os.path.join("static", filename)
    os.makedirs("static", exist_ok=True)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Informe del Hotel - {month:02}/{year}")

    c.setFont("Helvetica", 12)
    y = height - 100

    labels = {
        "total_recaudo": "Total Recaudado",
        "porcentaje_ocupacion": "Porcentaje de Ocupación",
        "promedio_dias": "Promedio de Días Reservados",
        "total_clientes": "Total de Clientes"
    }

    for key, label in labels.items():
        value = dashboard[key]
        if isinstance(value, float):
            value = round(value, 2)
        c.drawString(50, y, f"{label}: {value}")
        y -= 25

    c.save()
    return FileResponse(filepath, media_type="application/pdf", filename=filename)