from flask import Flask, request, render_template_string, jsonify, send_from_directory
import google.generativeai as genai
import variables  # Importamos las variables globales desde variables.py
import datosPrivados
import os
from crearImagen import send_to_colab  # Import the function


from chroma import replace_background
from remplazoFotogramas import reemplazar_imagenes
from unirFotogramas import create_video_from_images
from unirVideos import unir_videos_multiples
from sobreponerAudio import procesar_sonido
from unirAudioVideo import unir_video_audio

#nombreImagen=''

# Configuramos la API de Google Gemini
GOOGLE_API_KEY = datosPrivados.apiKeyGemini
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

# Ruta para mostrar el formulario
@app.route('/')
def index():
    return render_template_string(open('formulario.html').read())

# Ruta para procesar el formulario
@app.route('/procesar', methods=['POST'])
def procesar():
    promp = request.form['promp']

    # Concatenar los contextos con el promp recibido
    contexto = ' con base a lo anterior solo dame el verbo del tema que se está pidiendo , ejemplo: sumar, restar, multiplicar, dividir etc.'
    contexto2 = ' Tener en cuenta y que no se te olvide:  dame la palabra sin tildes, en singular, todo en minuscula y sin dieresis'
    contextoTemaFinal = promp + contexto + contexto2

    contextoAnimal = ' con base a lo anterior solo dame el animal que menciona'
    contextoAnimal2 = ' si no se menciona animal pero si menciona un lugar dame un animal correspondiente a ese lugar'
    contextoAnimal3 = ' si no menciona el animal ni el bioma, entoces dame un animal conocido para los niños'
    contextoAnimalFinal = promp + contextoAnimal + contextoAnimal2 + contextoAnimal3 + contexto2

    # Obtener respuestas de la API de Google Gemini
    respuestaTema = model.generate_content(contextoTemaFinal)
    variables.VariableTema = respuestaTema.text.strip()  # Asignar a la variable global y limpiar espacios

    respuestaAnimal = model.generate_content(contextoAnimalFinal)
    variables.VariableAnimal = respuestaAnimal.text.strip()  # Asignar a la variable global y limpiar espacios

    # Procesar el bioma y la descripción
    contextoFondo = ' con base a lo anterior solo dame el bioma, solo un bioma en singular, sin tildes y en minuscula, ejemplo: sabana,jungla,desierto,montaña etc'
    contextoFondo2 = ' si no se menciona el bioma pero si menciona el animal dame el bioma correspondiente a ese animal'
    contextoFondo3 = ' si no menciona bioma ni el animal, dame el bioma correspondiente a este animal: '
    contextoFondoFinal = promp + contextoFondo + contextoFondo2 + contextoFondo3 + variables.VariableAnimal +contexto2

    respuestaFondo = model.generate_content(contextoFondoFinal)
    variables.VariableFondo = respuestaFondo.text.strip()  # Asignar a la variable global y limpiar espacios

    contextoDescripcionFondo = ' con base al bioma mencionado anteriormente, dame una descripcion sencilla en ingles bajo esta estructura, ejemplo: Savannah landscape, Montain landscape etc.'
    fondoFinal = variables.VariableFondo + contextoDescripcionFondo

    respuestaDescripcion = model.generate_content(fondoFinal)
    variables.VariableDescripcionFondo = respuestaDescripcion.text.strip()  # Asignar a la variable global y limpiar espacios

    contextoDescripcionAnimal = ' con base al animal mencionado anteriormente, dame una descripcion sencilla en ingles bajo esta estructura, ejemplo: Animated lion, Animated cat etc.'
    animalFinal = variables.VariableAnimal + contextoDescripcionAnimal

    respuestaDescripcionAnimal = model.generate_content(animalFinal)
    variables.VariableDescripcionAnimal = respuestaDescripcionAnimal.text.strip()  # Asignar a la variable global y limpiar espacios



    # Imprimir las variables en la consola y devolver una respuesta
    print_variables()
    
    crearImagenIA()
    
    #chroma()
    
    #remplazo_fotogramas()
    
    #unirFotogramas()
    
    #unirVideos()
    
    #sobrePonerAudio()
    
    #unirVideoAudio()
    
    # Aquí debes agregar la lógica de procesamiento del video
    video_url = './videosCompletos/video_con_audioFINALOficial.mp4'  # Ruta relativa para el archivo
    return jsonify({'video_url': video_url})
   
    

    #return "Procesado e impreso en consola."
    
def crearImagenIA():

        
    #Crear Imagenes con IA
    nombreImagen='fondoNueva.png'
    send_to_colab("/content/fondoPaisaje.png", "/content/mascaraPaisaje.png", variables.VariableDescripcionFondo,nombreImagen)

    #Crear Animal

    nombreImagen='animalNueva.png'
    send_to_colab("/content/result_resized.png", "/content/mascaraAnimal.png", variables.VariableDescripcionAnimal,nombreImagen)

    #crear operacion

    if variables.VariableTema=='sumar':
        nombreImagen='operacionNueva.png'
        send_to_colab("/content/sumaOriginal.png", "/content/sumaMascara.png", variables.VariableDescripcionAnimal,nombreImagen)
        
    elif variables.VariableTema=='restar':
        nombreImagen='operacionNueva.png'
        send_to_colab("/content/sumaOriginal.png", "/content/sumaMascara.png", variables.VariableDescripcionAnimal,nombreImagen)
        
    elif variables.VariableTema=='multiplicar':
        nombreImagen='operacionNueva.png'
        send_to_colab("/content/sumaOriginal.png", "/content/sumaMascara.png", variables.VariableDescripcionAnimal,nombreImagen)
        
    elif variables.VariableTema=='dividir':
        nombreImagen='operacionNueva.png'
        send_to_colab("/content/dividirOriginal.png", "/content/mascaraDividir.png", variables.VariableDescripcionAnimal,nombreImagen) 
    else:
        #valor predeterminado la suma
        nombreImagen='operacionNueva.png'
        send_to_colab("/content/sumaOriginal.png", "/content/sumaMascara.png", variables.VariableDescripcionAnimal,nombreImagen)
        print('No se encontro tema')
        

def print_variables():
    """Función para imprimir las variables globales en la consola."""
    print(f"VariableTema: {variables.VariableTema}")
    print(f"VariableAnimal: {variables.VariableAnimal}")
    print(f"VariableFondo: {variables.VariableFondo}")
    print(f"VariableDescripcionFondo: {variables.VariableDescripcionFondo}")
    print(f"VariableDescripcionAnimal: {variables.VariableDescripcionAnimal}")

def chroma():
    
    if variables.VariableTema=='sumar':
        print('procesando Chroma....')
        
        #donde estamos
        replace_background(r'./chroma/ChromaSuma/pregunta.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyPreguntaNueva.png")
        #eso, estamos en la
        replace_background(r'./chroma/ChromaSuma/felicidad.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyFelicidadNueva.png")
        #saben cuales ese animal
        replace_background(r'./chroma/ChromaSuma/apuntarAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyApuntarNueva.png")
        #eso ese es un
        replace_background(r'./chroma/ChromaSuma/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png") 
        #pero que sonido hace
        replace_background(r'./chroma/ChromaSuma/preguntaAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyPregunta2Nueva.png")
        #eso ese es su sonido
        #replace_background(r'./chroma/ChromaSuma/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png")   
        #ahora veamos como sumar
        replace_background(r'./chroma/ChromaSuma/curioso.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyCuriosoNueva.png")
        
        #hora de sumar
        replace_background(r'./chroma/ChromaSuma/operacionSuma.png', r'./imagenesIA/operacionNueva.png', "./chromaNueva/boyOperacionNueva.png")
        
    
    elif variables.VariableTema=='restar':
        print('procesando Chroma....')
        #donde estamos
        replace_background(r'./chroma/ChromaResta/pregunta.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyPreguntaNueva.png")
        #eso, estamos en la
        replace_background(r'./chroma/ChromaResta/felicidad.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyFelicidadNueva.png")
        #saben cuales ese animal
        replace_background(r'./chroma/ChromaResta/apuntarAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyApuntarNueva.png")
        #eso ese es un
        replace_background(r'./chroma/ChromaResta/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png") 
        #pero que sonido hace
        replace_background(r'./chroma/ChromaResta/preguntaAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyPregunta2Nueva.png")
        #eso ese es su sonido
        #replace_background(r'./chroma/ChromaSuma/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png")   
        #ahora veamos como restar
        replace_background(r'./chroma/ChromaResta/curioso.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyCuriosoNueva.png")
        
        #hora de restar
        replace_background(r'./chroma/ChromaResta/operacionResta.png', r'./imagenesIA/operacionNueva.png', "./chromaNueva/boyOperacionNueva.png")
        

    elif variables.VariableTema=='multiplicar':
        print('procesando Chroma....')
            #donde estamos
        replace_background(r'./chroma/ChromaMultiplicar/pregunta.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyPreguntaNueva.png")
        #eso, estamos en la
        replace_background(r'./chroma/ChromaMultiplicar/felicidad.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyFelicidadNueva.png")
        #saben cuales ese animal
        replace_background(r'./chroma/ChromaMultiplicar/apuntarAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyApuntarNueva.png")
        #eso ese es un
        replace_background(r'./chroma/ChromaMultiplicar/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png") 
        #pero que sonido hace
        replace_background(r'./chroma/ChromaMultiplicar/preguntaAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyPregunta2Nueva.png")
        #eso ese es su sonido
        #replace_background(r'./chroma/ChromaSuma/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png")   
        #ahora veamos como restar
        replace_background(r'./chroma/ChromaMultiplicar/curioso.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyCuriosoNueva.png")
        
        #hora de restar
        replace_background(r'./chroma/ChromaMultiplicar/operacionMultiplicar.png', r'./imagenesIA/operacionNueva.png', "./chromaNueva/boyOperacionNueva.png")
       

    elif variables.VariableTema=='dividir':
        print('procesando Chroma....')
        #donde estamos
        replace_background(r'./chroma/ChromaDividir/pregunta.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyPreguntaNueva.png")
        #eso, estamos en la
        replace_background(r'./chroma/ChromaDividir/felicidad.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyFelicidadNueva.png")
        #saben cuales ese animal
        replace_background(r'./chroma/ChromaDividir/apuntarAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyApuntarNueva.png")
        #eso ese es un
        replace_background(r'./chroma/ChromaDividir/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png") 
        #pero que sonido hace
        replace_background(r'./chroma/ChromaDividir/preguntaAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyPregunta2Nueva.png")
        #eso ese es su sonido
        #replace_background(r'./chroma/ChromaSuma/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png")   
        #ahora veamos como restar
        replace_background(r'./chroma/ChromaDividir/curioso.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyCuriosoNueva.png")
    
        #hora de restar
        replace_background(r'./chroma/ChromaDividir/operacionDividir.png', r'./imagenesIA/operacionNueva.png', "./chromaNueva/boyOperacionNueva.png")
        
        
    else:
        print('procesando Chroma....')
        
        #donde estamos
        replace_background(r'./chroma/ChromaSuma/pregunta.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyPreguntaNueva.png")
        #eso, estamos en la
        replace_background(r'./chroma/ChromaSuma/felicidad.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyFelicidadNueva.png")
        #saben cuales ese animal
        replace_background(r'./chroma/ChromaSuma/apuntarAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyApuntarNueva.png")
        #eso ese es un
        replace_background(r'./chroma/ChromaSuma/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png") 
        #pero que sonido hace
        replace_background(r'./chroma/ChromaSuma/preguntaAnimal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyPregunta2Nueva.png")
        #eso ese es su sonido
        #replace_background(r'./chroma/ChromaSuma/felicidad2Animal.png', r'./imagenesIA/animalNueva.png', "./chromaNueva/boyFelicidad2Nueva.png")   
        #ahora veamos como sumar
        replace_background(r'./chroma/ChromaSuma/curioso.png', r'./imagenesIA/fondoNueva.png', "./chromaNueva/boyCuriosoNueva.png")
        
        #hora de sumar
        replace_background(r'./chroma/ChromaSuma/operacionSuma.png', r'./imagenesIA/operacionNueva.png', "./chromaNueva/boyOperacionNueva.png")
        print('No se encontro tema')
        print('Chroma finalizado')
    
def remplazo_fotogramas():
     
    # Ejemplo de uso:
    ruta_base = "./fotogramas/fotogramasParte2"
    imagen_reemplazo = "./chromaNueva/boyPreguntaNueva.png"

    reemplazar_imagenes(ruta_base, imagen_reemplazo)

    # Ejemplo de uso:
    ruta_base = "./fotogramas/fotogramasParte3"
    imagen_reemplazo = "./chromaNueva/boyFelicidadNueva.png"

    reemplazar_imagenes(ruta_base, imagen_reemplazo)

    #parte 4
    ruta_base = "./fotogramas/fotogramasParte4"
    imagen_reemplazo = "./chromaNueva/boyApuntarNueva.png"

    reemplazar_imagenes(ruta_base, imagen_reemplazo)

    #parte 5
    ruta_base = "./fotogramas/fotogramaParte5"
    imagen_reemplazo = "./chromaNueva/boyFelicidad2Nueva.png"

    reemplazar_imagenes(ruta_base, imagen_reemplazo)

    #parte 6
    ruta_base = "./fotogramas/fotogramaParte6"
    imagen_reemplazo = "./chromaNueva/boyPregunta2Nueva.png"

    reemplazar_imagenes(ruta_base, imagen_reemplazo)

    #parte 7
    ruta_base = "./fotogramas/fotogramaParte7"
    imagen_reemplazo = "./chromaNueva/boyFelicidad2Nueva.png"

    reemplazar_imagenes(ruta_base, imagen_reemplazo)

    #parte 8
    ruta_base = "./fotogramas/fotogramaParte8/"
    imagen_reemplazo = "./chromaNueva/boyCuriosoNueva.png"

    reemplazar_imagenes(ruta_base, imagen_reemplazo)

    #parte 9
    ruta_base = "./fotogramas/fotogramaParte9/"
    imagen_reemplazo = "./chromaNueva/boyOperacionNueva.png"

    reemplazar_imagenes(ruta_base, imagen_reemplazo)

    #parte 10,resultado

    if variables.VariableTema=='sumar':
    
        ruta_base = "./fotogramas/fotogramaParte10/"
        imagen_reemplazo = "./resultados/resultadoSuma.png"
        reemplazar_imagenes(ruta_base, imagen_reemplazo)   
    
    elif variables.VariableTema=='restar':
    
        ruta_base = "./fotogramas/fotogramaParte10/"
        imagen_reemplazo = "./resultados/resultadoResta.png"
        reemplazar_imagenes(ruta_base, imagen_reemplazo)
            
    elif variables.VariableTema=='multiplicar':
    
        ruta_base = "./fotogramas/fotogramaParte10/"
        imagen_reemplazo = "./resultados/resultadoMultiplicacion.png"
        reemplazar_imagenes(ruta_base, imagen_reemplazo)
    
    elif variables.VariableTema=='dividir':
    
        ruta_base = "./fotogramas/fotogramaParte10/"
        imagen_reemplazo = "./resultados/resultadoDivicion.png"
        reemplazar_imagenes(ruta_base, imagen_reemplazo)
    
    else:
        #valor predeterminado la suma
        ruta_base = "./fotogramas/fotogramaParte10/"
        imagen_reemplazo = "./resultados/resultadoSuma.png"
        reemplazar_imagenes(ruta_base, imagen_reemplazo)
        print('se toma el resultado predeterminado de suma')
    
    print('Remplazo finalizado') 
        
def unirFotogramas():
    create_video_from_images("./fotogramas/fotogramasParte2", "./videosNuevos/parte2.mp4")
    create_video_from_images("./fotogramas/fotogramasParte3", "./videosNuevos/parte3.mp4")
    create_video_from_images("./fotogramas/fotogramasParte4", "./videosNuevos/parte4.mp4")
    create_video_from_images("./fotogramas/fotogramaParte5", "./videosNuevos/parte5.mp4")
    create_video_from_images("./fotogramas/fotogramaParte6", "./videosNuevos/parte6.mp4")
    create_video_from_images("./fotogramas/fotogramaParte7", "./videosNuevos/parte7.mp4")
    create_video_from_images("./fotogramas/fotogramaParte8", "./videosNuevos/parte8.mp4")
    create_video_from_images("./fotogramas/fotogramaParte9", "./videosNuevos/parte9.mp4")
    create_video_from_images("./fotogramas/fotogramaParte10", "./videosNuevos/parte10.mp4")

def unirVideos():
    # Ejemplo de uso:
    videos = ["./videosNuevos/videoOrginalParte1.mp4","./videosNuevos/parte2.mp4", "./videosNuevos/parte3.mp4",
        "./videosNuevos/parte4.mp4", "./videosNuevos/parte5.mp4", "./videosNuevos/parte6.mp4",
        "./videosNuevos/parte7.mp4", "./videosNuevos/parte8.mp4","./videosNuevos/parte9.mp4", "./videosNuevos/parte10.mp4"
    ]
    video_final = "./videosCompletos/videoSinAudio.mp4"

    unir_videos_multiples(videos, video_final)
    
    
def sobrePonerAudio():
    # Ejemplo de uso   

    rutaTema=''
    

    if variables.VariableTema=='sumar':
        rutaTema='./audiobase/audioCompletoSuma.MP3'
        procesar_sonido(rutaTema, variables.VariableAnimal, 58000, 60000, "./audiosNueva/operacion1.mp3") 
        procesar_sonido("./audiosNueva/operacion1.mp3", variables.VariableAnimal+'s', 81000, 83000, "./audiosNueva/audioBase.mp3") 
        
    elif variables.VariableTema=='restar':
        rutaTema='./audiobase/audioCompletoResta.MP3'
        procesar_sonido(rutaTema, variables.VariableAnimal+'s', 59000, 61000, "./audiosNueva/operacion1.mp3") 
        procesar_sonido("./audiosNueva/operacion1.mp3", variables.VariableAnimal, 81000, 83000, "./audiosNueva/audioBase.mp3") 
        
    elif variables.VariableTema=='multiplicar':
        rutaTema='./audiobase/audioCompletoMultiplicar.MP3'
        procesar_sonido(rutaTema, variables.VariableAnimal+'s', 60000, 62000, "./audiosNueva/audioBase.mp3") 
        
    elif variables.VariableTema=='dividir':
        rutaTema='./audiobase/audioCompletoDividir.MP3' 
        procesar_sonido(rutaTema, 'silencio', 60000, 61000, "./audiosNueva/audioBase.mp3")   
    else:
        rutaTema='./audiobase/audioCompletoSuma.MP3'  
        procesar_sonido(rutaTema, variables.VariableAnimal, 58000, 60000, "./audiosNueva/operacion1.mp3") 
        procesar_sonido("./audiosNueva/operacion1.mp3", variables.VariableAnimal+'s', 81000, 83000, "./audiosNueva/audioBase.mp3") 
        
        
    procesar_sonido("./audiosNueva/audioBase.mp3", variables.VariableFondo, 16000, 19000, "./audiosNueva/audioParte1_superpuesto.mp3")   
    procesar_sonido("./audiosNueva/audioParte1_superpuesto.mp3", variables.VariableFondo, 22000, 25000, "./audiosNueva/audioParte2_superpuesto.mp3")   
    procesar_sonido("./audiosNueva/audioParte2_superpuesto.mp3", variables.VariableAnimal, 33000, 38000, "./audiosNueva/audioParte3_superpuesto.mp3")    
    procesar_sonido("./audiosNueva/audioParte3_superpuesto.mp3", variables.VariableAnimal +'_sonido', 46000, 49000, "./audiosNueva/audioFIN_superpuesto.mp3")    

        
 
        
       
def unirVideoAudio():
    video = "./videosCompletos/videoSinAudio.mp4"
    audio = "./audiosNueva/audioFIN_superpuesto.mp3"
    video_final = "./videosCompletos/video_con_audioFINALOficial.mp4"

    unir_video_audio(video, audio, video_final)
    
   

# Nueva ruta para devolver las variables en formato JSON
@app.route('/variables', methods=['GET'])
def obtener_variables():
    return jsonify({
        "VariableTema": variables.VariableTema,
        "VariableAnimal": variables.VariableAnimal,
        "VariableFondo": variables.VariableFondo,
        "VariableDescripcionFondo": variables.VariableDescripcionFondo,
        "VariableDescripcionAnimal": variables.VariableDescripcionAnimal
    })


# Ruta para servir el archivo de video desde una carpeta personalizada (en este caso, 'videosCompletos')
@app.route('/videosCompletos/<path:filename>')
def descargar_video(filename):
    video_dir = os.path.join(os.getcwd(), 'videosCompletos')  # Ruta completa de la carpeta 'videosCompletos'
    return send_from_directory(video_dir, filename)



if __name__ == '__main__':
    app.run(debug=True)




    



