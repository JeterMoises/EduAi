import requests
import variables 



def send_to_colab(img_url, mask_url, prompt,nombre):
  """Sends image processing request to Colab and downloads the result.

  Args:
      img_url (str): URL of the image to process.
      mask_url (str): URL of the mask image.
      prompt (str): Prompt for the image processing.

  Returns:
      None
  """

  colab_url = variables.conexionColab+"/process"  # Update with your Colab URL
  data = {
      "img_url": img_url,
      "mask_url": mask_url,
      "prompt": prompt,
      "nombre":nombre, 
  }
  response = requests.post(colab_url, json=data)

  if response.status_code == 200:
    result_url = response.json().get("result_url")
    print(f"Imagen procesada en: {result_url}")

    # Replace with your desired download logic (consider error handling)
    download_image(result_url, variables.miLocal+nombre)
  else:
    print(f"Error, Comunicarse con MOISES NEGRETE 3122642360: {response.status_code}")

def download_image(url, save_path):
  """Downloads an image from the provided URL.

  Args:
      url (str): URL of the image to download.
      save_path (str): Path to save the downloaded image.

  Returns:
      None
  """

  img_response = requests.get(url)
  if img_response.status_code == 200:
    with open(save_path, 'wb') as f:
      f.write(img_response.content)
    print(f"Imagen guardada en {save_path}")
  else:
    print(f"Error al descargar la imagen: {img_response.status_code}")