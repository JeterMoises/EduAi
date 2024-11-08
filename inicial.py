from sobreponerAudio import procesar_sonido
from unirAudioVideo import unir_video_audio

# Ejemplo de uso:
video = "./videosCompletos/videoSinAudio.mp4"
audio = "./audiosNueva/audioParte4_superpuesto.mp3"
video_final = "./videosCompletos/video_con_audioFINALOficial.mp4"

unir_video_audio(video, audio, video_final)