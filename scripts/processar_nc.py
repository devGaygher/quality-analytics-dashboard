"""
Processa o arquivo de exportação do Trello "GESTÃO DE NÃO CONFORMIDADES"
e gera uma planilha limpa apenas com os cartões da lista "MÊS ATUAL".

Uso:
    python processar_nc.py entrada.xlsx saida.xlsx

Colunas de entrada esperadas (exportação padrão do Trello):
    List | Title | Description | Points | Due | Members | Labels | Card # | Card URL

Colunas de saída:
    Data | Loja | Produto | Description | Labels
"""

import sys
import re
import unicodedata
from datetime import datetime

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment

# --------------------------------------------------------------------------
# Configurações / dicionários de apoio
# --------------------------------------------------------------------------

# Nome da lista do Trello que representa o mês em andamento
LISTA_MES_ATUAL = "MES ATUAL"

# Mapeamento de nomes/siglas de loja -> sigla final
MAPA_LOJAS = {f"L{i:02}": f"L{i:02}" for i in range(1, 7)}

# Categorias de Não Conformidade
CATEGORIAS_NC = {
    "PROBLEMA HIGIENICO SANITARIO",
    "VALIDADE",
    "PROBLEMAS DE FERMENTACAO",
    "EMBALAGEM FORA DO PADRAO",
    "PRODUTO FORA DO PADRAO",
    "AVARIAS DE TRANSPORTE",
}

DATA_REGEX = re.compile(r"^\d{1,2}/\d{1,2}(?:/\d{2,4})?$")


def normalizar(texto: str) -> str:
    """Maiúsculas, sem acento, sem espaços nas pontas — usado só para comparação."""
    if texto is None:
        return ""

    texto = str(texto).strip().upper()
    texto = unicodedata.normalize(
        "NFKD", texto
    ).encode("ASCII", "ignore").decode("ASCII")

    return texto


def converter_data(data_texto: str):
    """
    Converte a data encontrada no título para uma data real.

    Exemplos:
        05/08/2025 -> 05/08/2025
        5/8/2025   -> 05/08/2025
        05/08      -> 05/08/ano de referência (2025)

    Retorna uma data real do Python ou None se não for possível converter.
    """

    if not data_texto:
        return None

    data_texto = str(data_texto).strip()

    # Data com ano
    for formato in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(data_texto, formato)
        except ValueError:
            pass

    # Data sem ano -> utiliza o ano de referência (2025)
    try:
        data = datetime.strptime(data_texto, "%d/%m")
        return data.replace(year=2025)
    except ValueError:
        return None


def dividir_titulo(titulo: str):
    """
    Divide o título do card pelo separador '-'.

    Identifica automaticamente:
        Data
        Loja
        Produto

    Retorna:
        (data, loja, produto, precisa_revisao)
    """

    partes = [
        p.strip()
        for p in str(titulo).split("-")
        if p.strip() != ""
    ]

    partes = [p.upper() for p in partes]

    data_val = ""
    loja_val = ""
    revisao = False

    # 1) localizar a data
    restantes = []

    for p in partes:
        if not data_val and DATA_REGEX.match(p):
            data_val = p
        else:
            restantes.append(p)

    if not data_val:
        revisao = True

    # 2) localizar a loja
    sobra_final = []

    for p in restantes:
        if not loja_val:
            sigla = MAPA_LOJAS.get(normalizar(p))

            if sigla:
                loja_val = sigla
                continue

        sobra_final.append(p)

    if not loja_val:
        revisao = True

    # 3) o que sobrar é o produto
    produto_val = " - ".join(sobra_final).strip()

    if not produto_val:
        revisao = True

    # 4) converter data para data real
    data_convertida = converter_data(data_val)

    if data_val and data_convertida is None:
        revisao = True

    return data_convertida, loja_val, produto_val, revisao


def extrair_categoria_nc(labels: str):
    """
    Divide a coluna Labels original pelo separador ',' e retorna apenas
    a etiqueta que corresponde a uma categoria de Não Conformidade.
    """

    if pd.isna(labels) or str(labels).strip() == "":
        return "", True

    partes = [
        p.strip().upper()
        for p in str(labels).split(",")
        if p.strip() != ""
    ]

    encontradas = [
        p for p in partes
        if normalizar(p) in CATEGORIAS_NC
    ]

    if len(encontradas) == 0:
        return "", True

    # Se houver mais de uma categoria, fica a primeira
    return encontradas[0], len(encontradas) > 1


def processar(caminho_entrada: str, caminho_saida: str):

    # ----------------------------------------------------------------------
    # Ler arquivo do Trello
    # ----------------------------------------------------------------------

    df = (pd.read_csv(caminho_entrada, encoding="utf-8-sig")
          if str(caminho_entrada).lower().endswith(".csv")
          else pd.read_excel(caminho_entrada, sheet_name=0))

    # ----------------------------------------------------------------------
    # Verificar colunas necessárias
    # ----------------------------------------------------------------------

    colunas_necessarias = [
        "List",
        "Title",
        "Description",
        "Labels"
    ]

    faltando = [
        c for c in colunas_necessarias
        if c not in df.columns
    ]

    if faltando:
        raise ValueError(
            f"Colunas esperadas não encontradas no arquivo: {faltando}"
        )

    # ----------------------------------------------------------------------
    # 1) Filtrar pela lista "MÊS ATUAL"
    # ----------------------------------------------------------------------

    df = df[
        df["List"].apply(normalizar) == LISTA_MES_ATUAL
    ].copy()

    if df.empty:
        print(
            'Nenhuma linha encontrada com List = "MÊS ATUAL". Nada a gerar.'
        )
        return

    # ----------------------------------------------------------------------
    # 2) Separar título em Data / Loja / Produto
    # ----------------------------------------------------------------------

    resultado = df["Title"].apply(dividir_titulo)

    df["Data"] = resultado.apply(lambda r: r[0])
    df["Loja"] = resultado.apply(lambda r: r[1])
    df["Produto"] = resultado.apply(lambda r: r[2])

    revisar_titulo = resultado.apply(lambda r: r[3])

    # ----------------------------------------------------------------------
    # 3) Extrair categoria de NC da coluna Labels
    # ----------------------------------------------------------------------

    resultado_label = df["Labels"].apply(
        extrair_categoria_nc
    )

    df["Labels_NC"] = resultado_label.apply(
        lambda r: r[0]
    )

    revisar_label = resultado_label.apply(
        lambda r: r[1]
    )

    # ----------------------------------------------------------------------
    # 4) Montar planilha final
    # ----------------------------------------------------------------------

    final = df[
        [
            "Data",
            "Loja",
            "Produto",
            "Description",
            "Labels_NC"
        ]
    ].copy()

    final.columns = [
        "Data",
        "Loja",
        "Produto",
        "Description",
        "Labels"
    ]

    final["Description"] = final["Description"].fillna("")

    # ----------------------------------------------------------------------
    # 4.1) Garantir que Data seja reconhecida como data
    # ----------------------------------------------------------------------

    final["Data"] = pd.to_datetime(
        final["Data"],
        errors="coerce"
    )

    # ----------------------------------------------------------------------
    # 5) Salvar planilha
    # ----------------------------------------------------------------------

    final.to_excel(
        caminho_saida,
        index=False,
        sheet_name="Não Conformidades"
    )

    # ----------------------------------------------------------------------
    # 6) Formatação do Excel
    # ----------------------------------------------------------------------

    wb = load_workbook(caminho_saida)
    ws = wb.active

    # Fonte e alinhamento
    for row in ws.iter_rows():

        for cell in row:

            cell.font = Font(
                name="Arial",
                size=10,
                bold=(cell.row == 1)
            )

            cell.alignment = Alignment(
                vertical="top",
                wrap_text=(cell.row > 1)
            )

    # ----------------------------------------------------------------------
    # Formatação da coluna Data
    # ----------------------------------------------------------------------

    # A coluna A contém a Data
    for cell in ws["A"][1:]:
        cell.number_format = "dd/mm/yyyy"

    # ----------------------------------------------------------------------
    # Largura das colunas
    # ----------------------------------------------------------------------

    larguras = {
        "A": 12,
        "B": 10,
        "C": 28,
        "D": 60,
        "E": 30
    }

    for col, largura in larguras.items():
        ws.column_dimensions[col].width = largura

    # ----------------------------------------------------------------------
    # Salvar alterações
    # ----------------------------------------------------------------------

    wb.save(caminho_saida)

    # ----------------------------------------------------------------------
    # 7) Relatório de linhas que merecem revisão manual
    # ----------------------------------------------------------------------

    revisar = df[
        revisar_titulo.values |
        revisar_label.values
    ]

    print(
        f"Linhas processadas: {len(df)}"
    )

    print(
        f"Linhas que merecem revisão manual: {len(revisar)}"
    )

    if not revisar.empty:
        print("Linhas para revisão (índices):", list(revisar.index))


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 3:

        print(
            "Uso: python processar_nc.py entrada.xlsx saida.xlsx"
        )

        sys.exit(1)

    processar(
        sys.argv[1],
        sys.argv[2]
    )