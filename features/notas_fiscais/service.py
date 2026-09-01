from dataclasses import dataclass

from shared.pdf_reader import PDFReader
from features.notas_fiscais.parser import NotaFiscalParser
from features.notas_fiscais.model import NotaFiscal
from features.notas_fiscais.repository import NotaFiscalRepository

@dataclass(frozen=True)
class ResultadoProcessamento:
    encontradas: int
    adicionadas: int
    duplicadas: int

class NotaFiscalService:

    def __init__(self):
        self.reader =  PDFReader()
        self.parser = NotaFiscalParser()
        self.repository = NotaFiscalRepository()

    def processar_pdf(self, caminho_pdf: str) -> list[NotaFiscal]:
        pages = self.reader.read_pages(caminho_pdf)

        notas = []

        for page in pages:
            nota = self.parser.parse(page)

            if nota is not None:
                notas.append(nota)

        return notas

    def filtrar_duplicadas(self, notas: list[NotaFiscal], chaves_existentes: set[str]) -> list[NotaFiscal]:
        novas_notas = []
        chaves_conhecidas = set(chaves_existentes)

        for nota in notas:
            chave_normalizada = self._normalizar_chave(nota.chave)

            if not chave_normalizada:
                novas_notas.append(nota)
                continue

            if chave_normalizada in chaves_conhecidas:
                continue

            novas_notas.append(nota)
            chaves_conhecidas.add(chave_normalizada)

        return novas_notas

    def _normalizar_chave(self, chave: str | None) -> str:
        if chave is None:
            return ""

        return "".join(
            caractere
            for caractere in chave
            if caractere.isdigit()
        )

    def processar_e_salvar(self, caminho_pdf: str, caminho_planilha: str) -> ResultadoProcessamento:
        notas = self.processar_pdf(caminho_pdf)

        chaves_existentes = (self.repository.buscar_chaves_existentes(caminho_planilha))

        novas_notas = self.filtrar_duplicadas(notas, chaves_existentes)

        if novas_notas:
            self.repository.salvar(caminho_planilha, novas_notas)

        return ResultadoProcessamento(
            encontradas=len(notas),
            adicionadas=len(novas_notas),
            duplicadas=len(notas) - len(novas_notas)
        )