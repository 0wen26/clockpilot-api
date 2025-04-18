# clockpilot/database/crud/report_crud.py
from sqlalchemy.orm import Session
from database.models import Report, DaySummary, Shift
from core.utils import TimeConverter
from datetime import timedelta

def create_complete_report(db: Session, parsed_data: dict, user_id: int, month: int) -> Report:
    """
    Guarda un reporte completo con resúmenes diarios y turnos.

    Args:
        db: sesión de base de datos
        parsed_data: datos procesados del PDF
        user_id: identificador del usuario
        month: mes del reporte

    Returns:
        Report creado
    """
    totales = parsed_data["totals"]

    report = Report(
        user_id=user_id,
        horas_contrato=parsed_data["horas_contrato"],
        year=parsed_data["year"],
        month=month,
        total_hours=totales["total_hours"],
        total_hr_hours=totales["total_hr_hours"],
        complementary_hours=totales["complementary_hours"],
        total_festive_hours=totales["total_festive_hours"],
        total_sunday_hours=totales["total_sunday_hours"],
        total_early_days=int(totales["total_early_days"]),
        total_night_hours=totales["total_night_hours"],
        total_meal_allowance=int(totales["total_meal_allowance"]),
        total_split_shifts=int(totales["total_split_shifts"])
    )

    db.add(report)
    db.flush()

    conversor = TimeConverter()

    for fecha, dia in parsed_data["shifts_by_date"].items():
        resumen = DaySummary(
            report_id=report.id,
            fecha=fecha,
            duracion_total=conversor.timedelta_to_hh_mm(dia.get("duracion_total", "00:00"))
                if isinstance(dia.get("duracion_total"), timedelta)
                else dia.get("duracion_total", "00:00"),
            horas_perentorias=conversor.timedelta_to_hh_mm(dia.get("horas_perentorias"))
                if isinstance(dia.get("horas_perentorias"), timedelta)
                else dia.get("horas_perentorias", "00:00"),
            festive_hours=dia.get("festive_hours", "00:00"),
            horas_domingos=dia.get("horas_domingos", "00:00"),
            horas_madrugue=f"{int(dia.get('dias_madrugue', 0)):02d}",
            horas_nocturnas=dia.get("horas_nocturnas", "00:00"),
            manutencion=dia.get("viandas_comida", 0),
            fraccionadas=dia.get("turnos_fraccionados", 0),
        )
        db.add(resumen)
        db.flush()

        for turno in dia.get("turnos", []):
            shift = Shift(
                day_id=resumen.id,
                hora_entrada=turno["hora_entrada"],
                hora_salida=turno["hora_salida"],
                tipo=turno.get("tipo")
            )
            db.add(shift)

    db.commit()
    return report

def get_days_by_report(db: Session, report_id: int):
    """Obtiene todos los resúmenes diarios de un reporte."""
    return db.query(DaySummary).filter(DaySummary.report_id == report_id).all()

def get_shifts_by_report(db: Session, report_id: int):
    """Obtiene todos los turnos de un reporte."""
    return db.query(Shift).join(DaySummary).filter(DaySummary.report_id == report_id).all()
