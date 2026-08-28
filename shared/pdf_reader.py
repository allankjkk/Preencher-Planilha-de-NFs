import pdfplumber

class PDFReader:

    def read_pages(self, pdf_path: str) -> list[str]:
        pages = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                pages.append(text)

        return pages