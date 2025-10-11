import pandas as pd

def load_excel(path: str, header: int = 17) -> pd.DataFrame:
  # Lê todo o conteúdo a partir do cabeçalho
  df = pd.read_excel(path, sheet_name=0, header=header - 1)

  # Cria uma nova lista para armazenar apenas as linhas válidas
  valid_rows = []

  # Percorre linha por linha
  for i, row in df.iterrows():
    # Se a linha estiver completamente vazia
    if row.isnull().all():
      print(f"Linha {i + 2} está vazia. Parando a automação.")
      break
    else:
        valid_rows.append(row)

  # Converte a lista de volta para DataFrame
  df_clean = pd.DataFrame(valid_rows, columns=df.columns)

  return df_clean