from moviepy.editor import *

def unir_video_audio(video_path, audio_path, video_final):
    """
    Une un video y un audio en uno solo.

    Args:
        video_path (str): Ruta al archivo de video.
        audio_path (str): Ruta al archivo de audio.
        video_final (str): Nombre del video resultante.
    """

    # Cargar el video y el audio
    videoclip = VideoFileClip(video_path)
    audioclip = AudioFileClip(audio_path)

    # Asignar el audio al video
    videoclip.audio = audioclip

    # Guardar el video final
    videoclip.write_videofile(video_final, codec='libx264')

