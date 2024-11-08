from moviepy.editor import *
import os

def unir_videos_multiples(lista_videos, video_final):
    """
    Une múltiples videos en uno solo.

    Args:
        lista_videos (list): Lista de rutas a los videos.
        video_final (str): Nombre del video resultante.
    """

    try:
        # Verificar si los videos existen
        for video in lista_videos:
            if not os.path.exists(video):
                print(f"El archivo {video} no existe.")
                return

        # Cargar los videos
        clips = [VideoFileClip(video) for video in lista_videos]

        # Concatenar los clips
        final_clip = concatenate_videoclips(clips)

        # Verificar si la carpeta de salida existe, si no, crearla
        output_folder = os.path.dirname(video_final)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Guardar el video final
        final_clip.write_videofile(video_final, codec='libx264')
        print(f"Video final guardado en: {video_final}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

