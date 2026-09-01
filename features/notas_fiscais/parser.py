from features.notas_fiscais.model import NotaFiscal
import re
from datetime import datetime

def para_float(valor: str) -> float:
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    return float(valor)

class NotaFiscalParser:
    def parse(self, texto: str) -> NotaFiscal | None:
        chave = self.extrair_chave(texto)
        numero = self.extrair_numero(texto, chave)

        if not numero:
            return None

        return NotaFiscal(
            numero=numero,
            chave= chave,
            fornecedor=self.extrair_fornecedor(texto),
            cnpj=self.extrair_cnpj(texto),
            emissao=self.extrair_emissao(texto),
            valor=self.extrair_valor(texto),
            obra="",
            materiais=self.extrair_materiais(texto)
        )

    def extrair_numero(self, texto: str, chave: str | None) -> str | None:
        if chave and len(chave) >= 44:
            numero_chave = chave[25:34]

            return str(int(numero_chave))

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

    def extrair_emissao(self, texto: str) -> datetime | None:
        match = re.search(
            r"DATA DA EMISSÃO.*?(\d{4}-\d{2}-\d{2})",
        texto,
        re.DOTALL
        )

        if match:
            return datetime.strptime(match.group(1), "%Y-%m-%d")

        return None

    def extrair_materiais(self, texto: str) -> list[str]:
        bloco = re.search(
            r"CÓD\. PROD\..*?ALIQ\. IPI\n(.*?)CÁLCULO DO ISSQN",
            texto,
            re.DOTALL
        )

        if not bloco:
            return []

        materiais = []

        for linha in bloco.group(1).splitlines():
            match = re.match(
                r"^\d+\s+(.+?)\s+\d{8}\s+\d{3}\s+\d{4}\s+\S+",
                linha.strip()
            )

            if match:
                materiais.append(match.group(1).strip())

            if len(materiais) == 3:
                break

        return materiais

    def extrair_chave(self, texto: str) -> str | None:
        match = re.search(
            r"\d{2}-\d{4}-\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}-\d{2}-\d{3}-"
            r"\d{3}\.\d{3}\.\d{3}-\d{3}\.\d{3}\.\d{3}-\d",
            texto
        )

        if match:
            return re.sub(r"\D", "", match.group(0))

        return None

    def extrair_valor(self, texto: str) -> float | None:
        match = re.search(
            r"VALOR TOTAL DA NOTA\n([\d.,\s]+)\n",
            texto
        )

        if not match:
            return None

        valor = match.group(1).split()[-1]

        return para_float(valor)