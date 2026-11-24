# Guia de extração, tratamento e atualização

## 1. Extração

O fluxo original utiliza exportação tabular de cartões do Trello. Para esta demonstração, utilize `data/raw/trello_export_synthetic.csv`, sem acessar sistemas corporativos. A lista MÊS ATUAL é um marcador de seleção simulado, não uma afirmação de que todas as datas pertencem ao mesmo mês.

## 2. Tratamento

Instale as dependências e execute o comando descrito no README. O script valida colunas obrigatórias, filtra registros, identifica data/loja/produto no título, extrai a categoria de Labels e exporta uma planilha com Data, Loja, Produto, Description e Labels. Revise os índices sinalizados antes de importar.

Como alternativa manual, filtre a lista desejada, divida Title pelo hífen e Labels pela vírgula, reorganize data/loja/produto e selecione a categoria válida. Remova campos dispensáveis. Não exporte links ou informações pessoais para portfólio.

## 3. Classificação e carga

A etapa de setor e NC utiliza listas de validação; não é inferida pelo script. Para reproduzir a demonstração, abra `data/processed/dashboard_input.xlsx`, copie A2:H530 e cole apenas valores em C2 na aba BANCO DE DADOS de uma cópia do dashboard. Preserve cabeçalhos, tabela dados_trello, fórmulas e aba INDICADORES. Os IDs da base completa são sequenciais.

## 4. Atualização e análise

No Excel desktop, use Power Pivot > Gerenciar > Atualizar Tudo; retorne à planilha e use Dados > Atualizar Tudo. Limpe filtros e teste os hiperlinks, segmentações, gráficos e tabelas dinâmicas. Consulte GERAL e CATEGORIAS; SETORES está oculta na versão preservada. TABELAS e INDICADORES são abas de apoio. Não salve o painel por bibliotecas que não preservam Power Pivot.

## 5. Verificação antes da publicação

Confirme os 529 registros sem filtros, lojas L01–L06, ano 2025, ausência de dados antigos nos filtros e no modelo, integridade dos indicadores e ausência de mensagens de reparação. A estrutura do pacote foi verificada, mas o modelo binário exige revisão adicional. Verifique autorização de divulgação. Não inclua exportações reais, instruções internas, imagens ou credenciais.
