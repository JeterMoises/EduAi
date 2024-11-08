from PIL import Image

def replace_background(image_path, background_path, output_path):
  """
  Replaces the background of an image with another image.

  Args:
    image_path: Path to the foreground image.
    background_path: Path to the background image.
    output_path: Path to save the resulting image.
  """
  image = Image.open(image_path)
  imagenFondo = Image.open(background_path)

  width, height = image.size

  for i in range(width):
    for j in range(height):
      data = image.getpixel((i, j))
      data2 = imagenFondo.getpixel((i, j))

      # Check for green color as the foreground (adjust based on your image)
      if (data[1] > data[0] + data[2]):
        image.putpixel((i, j), data2)

  image.save(output_path)