import os
from core.security import create_access_token

def test_upload_pdf(client, test_user):
    # Obtener token válido para el usuario de prueba
    token = create_access_token(data={"sub": test_user.email})
    
    # Simula un archivo PDF
    test_pdf_path = "test.pdf"
    with open(test_pdf_path, "wb") as f:
        f.write(b"%PDF-1.4 fake pdf content")

    with open(test_pdf_path, "rb") as f:
        response = client.post(
            "/api/upload/upload",  # Añade el path completo
            files={"file": ("test.pdf", f, "application/pdf")},
            headers={"Authorization": f"Bearer {token}"}  # Usa token real
        )
    
    assert response.status_code == 200
    assert "procesado correctamente" in response.json()["message"]
    
    # Limpieza
    if os.path.exists(test_pdf_path):
        os.remove(test_pdf_path)