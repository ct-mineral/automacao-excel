import re

import pandas as pd

_ELEMENT_FROM_LINE = re.compile(r'^([A-Z][a-z]?)(?:\s*[KLM][a-z].*)?$')
_NUMBER = re.compile(r'[-+]?\d+(?:[.,]\d+)?(?:[eE][-+]?\d+)?')

def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
  return df.rename(columns={
    'Compound': 'Óxidos',
    'Analyte': 'Óxidos',
    'm/m%': '%',
    'Result': '%',
    'm/m%.1': '%%',
    'Int.(cps/uA)': 'Int. cps/uA',
    'El': 'Elementos',
    'Line': 'Elementos',
  })

def correction_datas(df: pd.DataFrame) -> pd.DataFrame:
  if 'Óxidos' in df.columns:
    df['Óxidos'] = df['Óxidos'].astype(str).str.strip()

  for column in ('%', '%%', 'Int. cps/uA'):
    if column in df.columns:
      df[column] = df[column].map(_to_number)

  if 'Elementos' in df.columns:
    df['Elementos'] = df['Elementos'].map(_element_symbol)

  return df

def _to_number(value):
  if pd.isna(value):
    return value
  if isinstance(value, (int, float)):
    return float(value)

  match = _NUMBER.search(str(value).strip())
  if not match:
    return pd.NA

  return float(match.group().replace(',', '.'))

def _element_symbol(value):
  if pd.isna(value):
    return value

  text = str(value).strip()
  match = _ELEMENT_FROM_LINE.match(text)
  if match:
    text = match.group(1)

  return {'Sx': 'S', 'Px': 'P'}.get(text, text)