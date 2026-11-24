# Dicionário de dados

| Campo no dashboard | Tipo | Descrição |
|---|---|---|
| ID | Inteiro | Identificador sintético único |
| DATA | Data | Data fictícia da ocorrência |
| LOJA | Texto | L01 a L06 |
| PRODUTO | Texto | Produto alimentício genérico |
| DESCRIÇÃO | Texto | Relato simulado |
| CATEGORIA | Texto | Categoria de não conformidade |
| SETOR | Texto | Setor responsável na classificação demonstrativa |
| NC | Texto | Tipo de não conformidade |

A entrada bruta contém List, Title, Description, Points, Due, Members, Labels, Card # e Card URL. Title combina data, loja e produto. Labels contém a categoria. Os campos opcionais Points, Due, Members e Card URL ficam vazios. A saída do ETL contém Data, Loja, Produto, Description e Labels. A base de carga acrescenta ID, SETOR e NC.
