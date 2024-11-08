#unir fotogramas
import os
from moviepy.editor import ImageClip, concatenate_videoclips

def create_video_from_images(image_folder, output_file, fps=24, duration=0.0416):
    """
    Crea un video a partir de una secuencia de imágenes en una carpeta.

    Args:
        image_folder (str): Ruta a la carpeta que contiene las imágenes.
        output_file (str, optional): Nombre del archivo de salida. Defaults to "output.mp4".
        fps (int, optional): Número de cuadros por segundo. Defaults to 24.
        duration (float, optional): Duración de cada imagen en segundos. Defaults to 0.0416.
    """

    try:
        # Verificar si la carpeta de imágenes existe
        if not os.path.exists(image_folder):
            print(f"La carpeta {image_folder} no existe.")
            return

        # Obtener una lista de todos los archivos en la carpeta
        image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

        # Verificar si hay imágenes en la carpeta
        if not image_files:
            print(f"No se encontraron imágenes en {image_folder}.")
            return

        # Ordenar los archivos por nombre (asumiendo un formato numérico secuencial)
        image_files.sort()

        # Crear una lista de clips de video a partir de las imágenes
        clips = [ImageClip(os.path.join(image_folder, img)).set_duration(duration) for img in image_files]

        # Concatenar los clips en un solo video
        video = concatenate_videoclips(clips, method="compose")

        # Verificar si la carpeta de salida existe, si no, crearla
        output_folder = os.path.dirname(output_file)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Escribir el archivo de video
        video.write_videofile(output_file, codec="libx264", fps=fps)
        print(f"Video guardado en: {output_file}")
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")