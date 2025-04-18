# clockpilot/api/routes/process.py

from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, List
import logging

from core.constants import FESTIVOS, SUNDAYS, MESES_MAP
from core.security import get_current_user
from core.calculations import (
    early_shifts,
    night_hours,
    festive_hours,
    sunday_hours,
    split_shifts,
    meal_allowance
)
from database.session import get_db
from database.crud.report_crud import create_complete_report
from api.schemas.report_schema import ReportFromDB, DaySummary, ReportResponse

router = APIRouter(tags=["Processing"])
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class ReportProcessor:
    def __init__(self, horas_contrato: int, year: int):
        self.horas_contrato = horas_contrato
        self.year = year

    def process_day(self, fecha: str, turnos: List[Dict]) -> DaySummary:
        is_festivo = self._is_festive_date(fecha)
        is_domingo = self._is_sunday_date(fecha)

        return DaySummary(
            fecha=fecha,
            turnos=turnos,
            duracion_total=self._calculate_total_hours(turnos),
            horas_perentorias=self._calculate_perentorias(turnos),
            festive_hours=self._calculate_total_hours(turnos) if is_festivo else "00:00",
            horas_domingos=self._calculate_total_hours(turnos) if is_domingo else "00:00",
            horas_madrugue=early_shifts.calculate_madrugue_hours({fecha: {"turnos": turnos}}),
            horas_nocturnas=night_hours.calculate_night_hours({fecha: {"turnos": turnos}}),
            manutencion=meal_allowance.calculate_meal_allowance({fecha: {"turnos": turnos}}),
            fraccionadas=split_shifts.calculate_split_shift({fecha: {"turnos": turnos}})
        )

    def _calculate_total_hours(self, turnos: List[Dict]) -> str:
        total = timedelta()
        for t in turnos:
            entrada = datetime.strptime(t["hora_entrada"], "%H:%M")
            salida = datetime.strptime(t["hora_salida"], "%H:%M")
            if salida <= entrada:
                salida += timedelta(days=1)
            total += salida - entrada
        return f"{total.seconds // 3600:02}:{(total.seconds % 3600) // 60:02}"

    def _calculate_perentorias(self, turnos: List[Dict]) -> str:
        return "00:00"

    def _is_festive_date(self, fecha: str) -> bool:
        try:
            dia, mes_nombre = fecha.split("-")
            mes = MESES_MAP.get(mes_nombre.lower())
            return f"{dia}-{mes}" in FESTIVOS.get(self.year, set())
        except:
            return False

    def _is_sunday_date(self, fecha: str) -> bool:
        try:
            dia, mes_nombre = fecha.split("-")
            mes = MESES_MAP.get(mes_nombre.lower())
            return f"{dia}-{mes}" in SUNDAYS.get(self.year, set())
        except:
            return False

@router.post("/process", response_model=ReportResponse)
async def process_pdf_data(
    dias: List[Dict],
    horas_contrato: int = Form(...),
    year: int = Form(...),
    month: int = Form(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    try:
        detalles = {dia["fecha"]: {"turnos": dia["turnos"]} for dia in dias}

        report_data = {
            "detalles": detalles,
            "horas_contrato": horas_contrato,
            "year": year,
            "month": month
        }

        ReportFromDB = create_complete_report(db, report_data, current_user.id)

        return ReportResponse(
            data=ReportFromDB,
            message="Procesamiento completado"
        )
    except Exception as e:
        logger.error(f"Error al procesar días: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al procesar los datos del PDF")
