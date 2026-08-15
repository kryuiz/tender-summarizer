from fastapi import FastAPI, File, HTTPException, UploadFile
from app.pdf import validate_pdf, extract_text
from app.llm import summarize_text

app = FastAPI(title='Tender Summarizer')

@app.get('/')
def root():
    return {'status': 'ok'}

@app.post('/upload')
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()

    try:
        validate_pdf(content)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    text = extract_text(content)
    summary = await summarize_text(text)

    return {
        'filename': file.filename,
        'size': len(content),
        'summary': summary
    }
