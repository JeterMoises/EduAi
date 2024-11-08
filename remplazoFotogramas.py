#remplazo de fotogramas
import os
import shutil

def reemplazar_imagenes(ruta_base, imagen_reemplazo):
  """
  Reemplaza todas las imágenes en una carpeta por una sola imagen.

  Args:
    ruta_base (str): Ruta base de las imágenes a reemplazar.
    imagen_reemplazo (str): Ruta de la imagen de reemplazo.
  """

  if not os.path.exists(imagen_reemplazo):
      print(f"Error: La imagen '{imagen_reemplazo}' no existe.")
      return

  # Obtener todos los archivos en la carpeta
  archivos = os.listdir(ruta_base)

  # Filtrar los archivos que correspondan al patrón "frame_X.png"
  frames = [int(f.split('_')[1].split('.')[0]) for f in archivos if f.startswith('frame_') and f.endswith('.png')]

  # Encontrar el último frame (asumiendo que los números de frame son consecutivos)
  ultimo_frame = max(frames) if frames else 0

  for i in range(ultimo_frame + 1):
      ruta_imagen_original = os.path.join(ruta_base, f"frame_{i}.png")
      try:
          shutil.copy2(imagen_reemplazo, ruta_imagen_original)
          print(f"Imagen {ruta_imagen_original} reemplazada.")
      except shutil.Error as e:
          print(f"Error al copiar la imagen: {e}")