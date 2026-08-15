from io import BytesIO
from pypdf import PdfReader

MAX_FILE_SIZE = 20 * 1024 ** 2

def validate_pdf(file_bytes: bytes) -> None:
    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError('File is too large')

    if not file_bytes.startswith(b"%PDF-"):
        raise ValueError('File is not a valid PDF')


def extract_text(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(file_bytes))
    except Exception as e:
        raise ValueError('Cannot read PDF') from e
    text = ''

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + '\n'

    return text.strip()
