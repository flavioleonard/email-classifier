from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from ..services.email_processor import EmailProcessor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

email_processor = EmailProcessor()

@app.post("/api/classify-email")
async def classify_email(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    try:
        email_content = ""
        if file:
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in ['.txt', '.pdf']:
                raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado")
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            try:
                email_content = email_processor.read_email_from_file(tmp_file_path, file_extension)
            finally:
                os.unlink(tmp_file_path)
        elif text:
            email_content = text
        else:
            raise HTTPException(status_code=400, detail="Nenhum conteúdo fornecido")
        result = email_processor.process_email(email_content)
        return {
            "category": result['category'],
            "confidence": round(result['confidence'], 2),
            "suggested_response": result['suggested_response'],
            "processed_text": result['processed_text'][:200] + "..." if len(result['processed_text']) > 200 else result['processed_text']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Email Classifier API is running"}