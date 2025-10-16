"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import pandas as pd
import io
import os
import re
# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    file_path = 'files/input/clusters_report.txt'

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo no se encontró en la ruta: {file_path}.")
    except Exception as e:
        raise Exception(f"Error al leer el archivo: {e}")

    data = io.StringIO(file_content)
    lines = data.readlines()

    col_names = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    data_rows = []
    current_row = {}

    data_lines = lines[4:]

    def clean_keywords(keywords_list):
        keywords_raw_string = " ".join(keywords_list)
        
        keywords_raw_string = re.sub(r'\s+', ' ', keywords_raw_string).strip()
        
        keywords_raw_string = keywords_raw_string.rstrip(".").rstrip(",").strip()
        
        keywords_raw_string = keywords_raw_string.replace(" ,", ",").replace(":", ",")
        
        keywords = [k.strip() for k in keywords_raw_string.split(',')]
        
        keywords = [k for k in keywords if k]
        
        return ", ".join(keywords)

    for line in data_lines:
        line = line.strip()
        if not line:
            continue

        if line and line.split()[0].isdigit():
            if current_row:
                current_row[col_names[3]] = clean_keywords(current_row[col_names[3]])
                data_rows.append(current_row)

            parts = line.split()
            cluster = parts[0]
            cantidad = parts[1]
            
            end_of_cantidad = line.find(cantidad) + len(cantidad)
            porcentaje_y_resto = line[end_of_cantidad:].strip()
            
            match_keyword = re.search(r'[a-zA-Z\(\-\/]+', porcentaje_y_resto)

            if match_keyword:
                start_of_keywords = match_keyword.start()
                porcentaje_raw = porcentaje_y_resto[:start_of_keywords].strip()
                keywords_raw = porcentaje_y_resto[start_of_keywords:].strip()
            else:
                porcentaje_raw = porcentaje_y_resto.strip()
                keywords_raw = ""
            
            porcentaje_limpio = porcentaje_raw.replace('%', '').replace(',', '.').strip()
            porcentaje_float = float(porcentaje_limpio)


            current_row = {
                col_names[0]: int(cluster),
                col_names[1]: int(cantidad),
                col_names[2]: porcentaje_float, 
                col_names[3]: [keywords_raw] 
            }
        else:
            keywords_raw = line.strip()
            if col_names[3] in current_row:
                current_row[col_names[3]].append(keywords_raw)

    if current_row:
        current_row[col_names[3]] = clean_keywords(current_row[col_names[3]])
        data_rows.append(current_row)

    df = pd.DataFrame(data_rows, columns=col_names)

    return df