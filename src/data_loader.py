import re

import pandas as pd

_RESULT_ROW = re.compile(
  r'^(?P<analyte>\S+)\s+'
  r'(?P<result>[-+]?\d+(?:[.,]\d+)?(?:[eE][-+]?\d+)?)\s*%\s+'
  r'\[[^\]]*\]\s+\S+\s+'
  r'(?P<line>.+?)\s+'
  r'(?P<intensity>[-+]?\d+(?:[.,]\d+)?(?:[eE][-+]?\d+)?)\s*,?\s*$'
)

def load_file(path: str, header: int = 17) -> pd.DataFrame:
  if str(path).lower().endswith('.csv'):
    return load_csv(path)
  return load_excel(path, header=header)

def load_csv(path: str) -> pd.DataFrame:
  # Relatório do EDX: o cabeçalho Analyte não fica numa linha fixa.
  rows = []
  started = False

  with open(path, encoding='utf-8', errors='replace') as file:
    for raw_line in file:
      line = raw_line.strip().rstrip(',').strip()
      if not started:
        if line.startswith('Analyte'):
          started = True
        continue
      if not line or set(line) <= {'-'}:
        continue

      match = _RESULT_ROW.match(line)
      if not match:
        continue

      rows.append({
        'Analyte': match.group('analyte'),
        'Result': match.group('result'),
        'Line': match.group('line').strip(),
        'Int.(cps/uA)': match.group('intensity'),
      })

  if not rows:
    raise ValueError('Nenhum resultado de Analyte encontrado no CSV.')

  return pd.DataFrame(rows)

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