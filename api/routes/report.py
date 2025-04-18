# clockpilot/api/routes/report.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.session import get_db
from database.models import Report as DBReport, User
from database.crud.report_crud import create_complete_report
from database.schemas.report_schema import ReportCreate, ReportUpdateSchema
from api.schemas.report_schema import ReportListResponse, ReportResponse
from api.schemas.response import ErrorResponse, ApiResponse
from core.security import get_current_user
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{report_id}/summary")
def get_report_summary(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(DBReport).filter(DBReport.id == report_id, DBReport.user_id == current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    user = db.query(User).filter(User.id == report.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "report_id": report.id,
        "user_email": user.email,
        "year": report.year,
        "month": report.month,
        "horas_contrato": report.horas_contrato,
        "total_hours": report.total_hours,
        "total_hr_hours": report.total_hr_hours,
        "complementary_hours": report.complementary_hours,
        "total_festive_hours": report.total_festive_hours,
        "total_sunday_hours": report.total_sunday_hours,
        "total_early_days": report.total_early_days,
        "total_night_hours": report.total_night_hours,
        "total_meal_allowance": report.total_meal_allowance,
        "total_split_shifts": report.total_split_shifts,
        "created_at": report.created_at,
    }


@router.get("/reports/{report_id}/daily", response_model=ApiResponse)
def get_daily_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(DBReport).options(joinedload(DBReport.day_summaries))\
        .filter(DBReport.id == report_id, DBReport.user_id == current_user.id)\
        .first()

    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    daily_data = []
    for day in sorted(report.day_summaries, key=lambda d: d.fecha):
        daily_data.append({
            "fecha": day.fecha,
            "duracion_total": day.duracion_total,
            "horas_perentorias": day.horas_perentorias,
            "festive_hours": day.festive_hours,
            "horas_domingos": day.horas_domingos,
            "horas_madrugue": day.horas_madrugue,
            "horas_nocturnas": day.horas_nocturnas,
            "manutencion": day.manutencion,
            "fraccionadas": day.fraccionadas
        })

    return ApiResponse(success=True, message="Resumen diario generado", data=daily_data)



@router.post("/", response_model=ReportResponse)
def create_new_report(
    report: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        created_report = create_complete_report(
            db=db,
            parsed_data=report.model_dump(),
            user_id=current_user.id
        )
        return ReportResponse(
            data=created_report,
            message="Reporte creado exitosamente"
        )
    except Exception as e:
        logger.error(f"Error al crear reporte: {str(e)}", exc_info=True)
        return ErrorResponse(
            message="Error al crear el reporte",
            error_code="REPORT_001",
            success=False
        )


@router.get("/{report_id}", response_model=ReportResponse)
def read_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        db_report = db.query(DBReport).filter(
            DBReport.id == report_id,
            DBReport.user_id == current_user.id
        ).first()

        if not db_report:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")

        return ReportResponse(data=db_report)

    except Exception as e:
        logger.error(f"Error al obtener reporte {report_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=ReportListResponse)
def read_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        reports = db.query(DBReport).filter(DBReport.user_id == current_user.id).offset(skip).limit(limit).all()
        return ReportListResponse(
            data=reports,
            message=f"Obtenidos {len(reports)} reportes"
        )
    except Exception as e:
        logger.error(f"Error al listar reportes: {str(e)}", exc_info=True)
        return ErrorResponse(
            message="Error al obtener los reportes",
            error_code="REPORT_003",
            success=False
        )


@router.delete("/{report_id}", status_code=204)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(DBReport).filter_by(id=report_id, user_id=current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    db.delete(report)
    db.commit()
    return


@router.put("/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    update_data: ReportUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(DBReport).filter_by(id=report_id, user_id=current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(report, field, value)

    db.commit()
    db.refresh(report)
    return ReportResponse(data=report)
