from shared.pdf_reader import PDFReader
from features.notas_fiscais.parser import NotaFiscalParser


def main():
    print("1 - iniciou")

    reader = PDFReader()
    print("2 - criou PDFReader")

    parser = NotaFiscalParser()
    print("3 - criou parser")

    pages = reader.read_pages("teste.pdf")
    print(f"4 - leu PDF: {len(pages)} página(s)")

    texto = pages[0]
    print(f"5 - texto extraído: {len(texto)} caracteres")

    numero = parser.extrair_numero(texto)
    print(f"6 - número: {numero}")

    fornecedor = parser.extrair_fornecedor(texto)
    print(f"7 - fornecedor: {fornecedor}")

    cnpj = parser.extrair_cnpj(texto)
    print(f"8 - CNPJ: {cnpj}")


if __name__ == "__main__":
    main()