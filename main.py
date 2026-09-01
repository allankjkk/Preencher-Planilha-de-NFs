from features.notas_fiscais.service import NotaFiscalService


def main():
    service = NotaFiscalService()

    try:
        resultado = service.processar_e_salvar(
            "teste.pdf",
            "PORTAL ADM - Teste.xlsx"
        )

        print(
            f"Notas encontradas: "
            f"{resultado.encontradas}"
        )
        print(
            f"Notas adicionadas: "
            f"{resultado.adicionadas}"
        )
        print(
            f"Duplicadas ignoradas: "
            f"{resultado.duplicadas}"
        )

    except FileNotFoundError as erro:
        print(
            f"Arquivo não encontrado: "
            f"{erro.filename}"
        )

    except PermissionError:
        print(
            "Não foi possível acessar a planilha. "
            "Verifique se ela está aberta no Excel."
        )

    except KeyError:
        print(
            'A aba "Conferência" não foi encontrada '
            "na planilha."
        )


if __name__ == "__main__":
    main()