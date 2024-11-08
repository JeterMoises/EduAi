from pydub import AudioSegment
#import os

# Especifica la ruta donde está instalado FFmpeg
#os.environ["PATH"] += os.pathsep + "C:\ffmpeg"

# Ahora puedes usar pydub normalmente



def superponer_y_guardar_audio(videoBase, audioSobreponer, inicio, fin, nombreArchivo):
    """Superpone un audio sobre otro en un rango específico y guarda el resultado.

    Args:
        videoBase: Ruta del archivo de audio base.
        audioSobreponer: Ruta del archivo de audio a superponer.
        inicio: Tiempo de inicio (en milisegundos) de la superposición.
        fin: Tiempo de fin (en milisegundos) de la superposición.
        nombreArchivo: Nombre del archivo de audio resultante.
    """
    # Cargar los audios
    musica = AudioSegment.from_mp3(videoBase)
    sonido = AudioSegment.from_mp3(audioSobreponer)

    # Asegurar que el sonido no sea más largo que el rango de superposición
    sonido = sonido[:fin - inicio]

    # Cortar la sección de la música donde se superpondrá el sonido
    seccion_musica = musica[inicio:fin]

    # Superponer el sonido sobre la sección de la música
    seccion_combinada = seccion_musica.overlay(sonido)

    # Reemplazar la sección de la música con la sección combinada
    musica_final = musica[:inicio] + seccion_combinada + musica[fin:]

    # Guardar el archivo final
    musica_final.export(nombreArchivo, format="mp3")
    print(f"Audio guardado con éxito: {nombreArchivo}")

# Diccionario para mapear palabras clave con archivos de audio
sonidos = {
    
    #Bioma
    "sabana":"./audioKidBioma/sabana.MP3",   
    "jungla": "./audioKidBioma/jungla.mp3",
    "montaña":"./audioKidBioma/montaña.MP3",
    "pradera":"./audioKidBioma/pradera.MP3",
    "tundra":"./audioKidBioma/tundra.MP3",
    "bosque":"./audioKidBioma/bosque.MP3",
    "desierto":"./audioKidBioma/desierto.MP3",
    "granja":"./audioKidBioma/granja.MP3",
    
    #animales niños
    "burro":"./audioKidAnimales/burro.MP3",
    "caballo":"./audioKidAnimales/caballo.MP3",
    "cerdo":"./audioKidAnimales/cerdo.MP3",
    "elefante":"./audioKidAnimales/elefante.MP3",
    "gato":"./audioKidAnimales/gato.MP3",
    "mono": "./audioKidAnimales/mono.mp3",
    "oso":"./audioKidAnimales/oso.MP3",
    "oveja":"./audioKidAnimales/oveja.MP3",
    "pato":"./audioKidAnimales/pato.MP3",
    "perro":"./audioKidAnimales/perro.MP3",
    "pinguino":"./audioKidAnimales/pinguino.MP3",
    "pingüino":"./audioKidAnimales/pinguino.MP3",
    "serpiente":"./audioKidAnimales/serpiente.MP3",
    "vaca":"./audioKidAnimales/vaca.MP3",
    "leon":"./audioKidAnimales/leon.MP3",
    
    #animales niños plural
    "burros":"./audioKidAnimales/burros.MP3",
    "caballos":"./audioKidAnimales/caballos.MP3",
    "cerdos":"./audioKidAnimales/cerdos.MP3",
    "elefantes":"./audioKidAnimales/elefantes.MP3",
    "gatos":"./audioKidAnimales/gatos.MP3",
    "monos": "./audioKidAnimales/monos.mp3",
    "osos":"./audioKidAnimales/osos.MP3",
    "ovejas":"./audioKidAnimales/ovejas.MP3",
    "patos":"./audioKidAnimales/patos.MP3",
    "perros":"./audioKidAnimales/perros.MP3",
    "pinguinos":"./audioKidAnimales/pinguinos.MP3",
    "pingüinos":"./audioKidAnimales/pinguinos.MP3",
    "serpientes":"./audioKidAnimales/serpientes.MP3",
    "vacas":"./audioKidAnimales/vacas.MP3",
    "leons":"./audioKidAnimales/leons.MP3",
    

    
    #Sonido de animales
    "burro_sonido":"./audiosAnimales/Burro.mp3",
    "caballo_sonido":"./audiosAnimales/Caballo.mp3",
    "cerdo_sonido":"./audiosAnimales/Cerdo.mp3",
    "elefante_sonido":"./audiosAnimales/Elefante.mp3",
    "gato_sonido":"./audiosAnimales/Gato.mp3",
    "mono_sonido": "./audiosAnimales/Mono.mp3",
    "oso_sonido":"./audiosAnimales/Oso.mp3",
    "oveja_sonido":"./audiosAnimales/Oveja.mp3",
    "pato_sonido":"./audiosAnimales/Pato.mp3",
    "perro_sonido":"./audiosAnimales/Perro.mp3",
    "pinguino_sonido":"./audiosAnimales/Pinguino.mp3",
    "pingüino_sonido":"./audiosAnimales/Pinguino.mp3",
    "serpiente_sonido":"./audiosAnimales/Serpiente.mp3",
    "vaca_sonido":"./audiosAnimales/Vaca.mp3",
    
    "silencio":"./audiosAnimales/silencio.MP3",
    
    
}
'''''
# Lógica del bucle para seleccionar el sonido y generar el archivo
def procesar_sonido(videoBase, palabra_clave, inicio, fin, nombreArchivo):
    if palabra_clave in sonidos:
        audioSobreponer = sonidos[palabra_clave]
        try:
            superponer_y_guardar_audio(videoBase, audioSobreponer, inicio, fin, nombreArchivo)
        except Exception as e:
            print(f"Error al procesar el audio: {e}")
    else:
        print("Palabra clave no encontrada.")

'''
def procesar_sonido(videoBase, palabra_clave, inicio, fin, nombreArchivo):
    if palabra_clave in sonidos:
        audioSobreponer = sonidos[palabra_clave]
        try:
            superponer_y_guardar_audio(videoBase, audioSobreponer, inicio, fin, nombreArchivo)
        except Exception as e:
            print(f"Error al procesar el audio: {e}")
    else:
        audioSobreponer = sonidos['silencio']
        try:
            superponer_y_guardar_audio(videoBase, audioSobreponer, inicio, fin, nombreArchivo)
        except Exception as e:
            print(f"Error al procesar el audio: {e}")
            
        #print("Palabra clave no encontrada.")  
