from features.notas_fiscais.model import NotaFiscal
import re


class NotaFiscalParser:
    def parse(self, texto: str) -> NotaFiscal:
        pass

    def extrair_numero(self, texto: str) -> str:
        match = re.search(
            r"N[º°]?\s*\.?:?\s*(\d+)",
            texto
        )

        if match:
            return match.group(1)

        return None

    def extrair_fornecedor(self, texto: str) -> str | None:
        match = re.search(
             r"Identificação do Emitente.*?\n(.+?)\s+Documento Auxiliar",
            texto,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        return None

    def extrair_cnpj(self, texto: str) -> str | None:
        match = re.search(
            r"CNPJ/CPF.*?\n.*?(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})",
            texto,
            re.DOTALL
            )

        if match:
            return match.group(1)

        return None