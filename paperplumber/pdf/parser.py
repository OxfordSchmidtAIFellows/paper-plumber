from pdfminer.high_level import extract_text


class PDFParser:

    def parse(self, file_path: str) -> str:
        """Parse PDF file and return text."""
        return self.sanitize(extract_text(file_path))
    
    def sanitize(self, text: str) -> str:
        text = text.replace('\n', ' ')
        text = text.replace('\x0c', ' ')
        return text
