import os
import easyocr
from tqdm import tqdm

def extraer_texto_de_imagen(ruta_imagen, lector):
    try:
        resultados = lector.readtext(ruta_imagen, detail=0, paragraph=True)
        texto = '\n'.join(resultados)
        return texto
    except Exception as e:
        print(f"Error al procesar {ruta_imagen}: {e}")
        return ""

def procesar_carpeta(carpeta, lector, extensiones):
    textos = []
    archivos = [archivo for archivo in os.listdir(carpeta) if archivo.lower().endswith(extensiones)]
    
    if not archivos:
        return  # No hay imágenes en esta carpeta

    print(f"Procesando carpeta: {carpeta}")
    for archivo in tqdm(archivos, desc=f"Procesando imágenes en {os.path.basename(carpeta)}"):
        ruta_completa = os.path.join(carpeta, archivo)
        texto_extraido = extraer_texto_de_imagen(ruta_completa, lector)
        textos.append(f"--- Texto de {archivo} ---\n{texto_extraido}\n")

    # Define el nombre del archivo de texto para la carpeta
    ruta_txt = os.path.join(carpeta, "texto_extraido.txt")

    # Escribe todo el texto extraído en el archivo .txt
    with open(ruta_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(textos))

def main():
    # Ruta de la carpeta que contiene las imágenes
    carpeta_imagenes = "/home/steven/Descargas/Caso74"  # <-- Actualiza esta ruta

    # Extensiones de archivos de imagen que deseas procesar
    extensiones = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')

    # Inicializa el lector de EasyOCR (especifica el idioma según tus necesidades, por ejemplo 'es' para español)
    lector = easyocr.Reader(['es'], gpu=False)  # Cambia a True si tienes una GPU compatible

    # Recorre todas las subcarpetas y archivos en la carpeta de imágenes
    for raiz, dirs, archivos in os.walk(carpeta_imagenes):
        # Procesa cada carpeta que contiene imágenes
        tiene_imagenes = any(archivo.lower().endswith(extensiones) for archivo in archivos)
        if tiene_imagenes:
            procesar_carpeta(raiz, lector, extensiones)

    print("Proceso completado.")

if __name__ == "__main__":
    main()
