# clockpilot/api/routes/upload.py
from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
import tempfile, os, time, logging
from typing import Dict, Any

from core.file_processing.pdf_processor import PDFProcessor
from database.session import get_db
from database.models import User
from core.security import get_current_user
from database.crud.report_crud import create_complete_report

router = APIRouter(tags=["Upload"])
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_file(
    file: UploadFile,
    horas_contrato: int = Form(...),
    year: int = Form(...),
    month: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF")

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            temp_path = tmp.name

        pdf_parser = PDFProcessor(year)
        parsed = pdf_parser.process_pdf(temp_path, horas_contrato)

        parsed["horas_contrato"] = horas_contrato
        parsed["year"] = year
        parsed["month"] =month
        report = create_complete_report(db, parsed, current_user.id,month)


        return {
            "status": "success",
            "report_id": report.id,
            "message": "PDF procesado y guardado correctamente"
        }

    except Exception as e:
        logger.error(f"❌ Error procesando PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno al procesar el PDF")

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"No se pudo eliminar archivo temporal: {str(e)}")
