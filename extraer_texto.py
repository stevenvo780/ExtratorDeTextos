import os
import easyocr
from tqdm import tqdm

def extraer_texto_de_imagen(ruta_imagen, lector):
    try:
        resultados = lector.readtext(ruta_imagen, detail=0, paragraph=True, contrast_ths=0.7, adjust_contrast=0.5)
        return '\n'.join(resultados)
    except Exception as e:
        print(f"Error al procesar {ruta_imagen}: {e}")
        return ""

def procesar_carpeta(carpeta, lector, extensiones):
    textos = []
    archivos = [archivo for archivo in os.listdir(carpeta) if archivo.lower().endswith(extensiones)]
    if not archivos:
        return
    for archivo in tqdm(archivos, desc=f"Procesando imágenes en {os.path.basename(carpeta)}"):
        ruta_completa = os.path.join(carpeta, archivo)
        texto_extraido = extraer_texto_de_imagen(ruta_completa, lector)
        textos.append(f"--- Texto de {archivo} ---\n{texto_extraido}\n")
    ruta_txt = os.path.join(carpeta, "texto_extraido.txt")
    with open(ruta_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(textos))

def main():
    carpeta_imagenes = "/home/steven/Descargas/Caso74"
    extensiones = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
    lector = easyocr.Reader(['es'], gpu=True, model_storage_directory='./models', download_enabled=True)
    for raiz, dirs, archivos in os.walk(carpeta_imagenes):
        tiene_imagenes = any(archivo.lower().endswith(extensiones) for archivo in archivos)
        if tiene_imagenes:
            procesar_carpeta(raiz, lector, extensiones)
    print("Proceso completado.")

if __name__ == "__main__":
    main()
