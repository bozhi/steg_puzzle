#!env/bin/python3
import argparse

from PIL import Image

ORIGINAL_BITS = 0b11111100
HIDE_BITS     = 0b00000011

def load_payload(pixel, pixel_payload):
  return (pixel & ORIGINAL_BITS) | pixel_payload

def generate_payload_for_size(row_len, col_len):
  payload = []
  for i in range(0, 32, 2):
    red_payload = (row_len >> i) & HIDE_BITS
    green_payload = (col_len >> i) & HIDE_BITS
    payload.append( (red_payload, green_payload, 0) )
  return payload

def extract_size_from_payload(payload):
  row_len = 0
  col_len = 0
  for i in range(16):
    row_len |= (payload[i][0] & HIDE_BITS) << (i * 2)
    col_len |= (payload[i][1] & HIDE_BITS) << (i * 2)
  return (row_len, col_len)

def generate_payload_from_pixel(pixel):
  r,g,b = pixel
  payload = []
  payload.append(( (r >> 6) & HIDE_BITS, (g >> 6) & HIDE_BITS, (b >> 6) & HIDE_BITS))
  payload.append(( (r >> 4) & HIDE_BITS, (g >> 4) & HIDE_BITS, (b >> 4) & HIDE_BITS))
  return payload

def extract_pixel_from_payload(payload):
  r = g = b = 0
  r |= payload[0][0] << 6 | payload[1][0] << 4
  g |= payload[0][1] << 6 | payload[1][1] << 4
  b |= payload[0][2] << 6 | payload[1][2] << 4
  return (r, g, b)

def process_payload(payload_image):
  payload_row_len = payload_image.size[0]
  payload_col_len = payload_image.size[1]
  pixel_payload = []

  # Storing the size of the hidden image in the first 16 pixels
  pixel_payload.extend(generate_payload_for_size(payload_row_len, payload_col_len))

  # Sanity check to make sure that what we put in is what we get out
  if extract_size_from_payload(pixel_payload) != payload_image.size:
    raise Exception("Incorrect size stored")

  # Encoding the payload image
  for row in range(payload_row_len):
    for col in range(payload_col_len):
      pixel = payload_image.getpixel((row, col))
      payload = generate_payload_from_pixel(pixel)
      retrieved = extract_pixel_from_payload(payload)
      # Sanity check that the encoding of pixel was done correctly
      if (pixel[0] & 240, pixel[1] & 240, pixel[2] & 240) != retrieved:
        raise Exception("Encoding error")
      pixel_payload.extend(payload)

  return pixel_payload

def encrypt(original_image_path, payload_image_path, output_filepath):
  original_image = Image.open(original_image_path)
  payload_image = Image.open(payload_image_path)

  # Sanity Check to make sure that the size of the image fits
  if original_image.size[0] * original_image.size[1] < payload_image.size[0] * payload_image.size[1] * 2:
    raise Exception("Unable to hide the payload completely")

  # Getting image data to hide
  payload_data = process_payload(payload_image)

  idx = 0
  new_image = Image.new(
      "RGB",
      (original_image.size[0], original_image.size[1]),
      color="white")

  # Looping over base image
  for row in range(original_image.size[0]):
    for col in range(original_image.size[1]):
      red, green, blue = original_image.getpixel((row, col))
      if idx < len(payload_data):
        # Add data to hide only when there is data to hide
        red_payload, green_payload, blue_payload = payload_data[idx]
        new_image.putpixel(
            (row,col),
            (load_payload(red, red_payload),
             load_payload(green, green_payload),
             load_payload(blue, blue_payload)))
        idx += 1
      else:
        new_image.putpixel(
            (row,col),
            (red, green, blue))
  new_image.save(output_filepath, "png")
  new_image.close()

def decrypt(steg_image_path, output_filepath):
  '''
    To solve the puzzle, reverse engineer above to figure it out
  '''
  pass


def main(args):
  original_image_path = args.original_image
  payload_image_path = args.payload_image
  steg_image_path = args.steg_image
  output_filepath = args.output_filepath
  mode = args.mode
  if mode == "encrypt":
    encrypt(original_image_path, payload_image_path, output_filepath)
  elif mode == "decrypt":
    decrypt(steg_image_path, output_filepath)
  else:
    print("Unknown mode {}".format(mode))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Puzzle for Wennee")
  parser.add_argument("--mode", type=str, help="encrypt or decrypt")
  parser.add_argument("--original_image", type=str, help="Original image path")
  parser.add_argument("--payload_image", type=str, help="Payload image path")
  parser.add_argument("--steg_image", type=str, help="Steganographed image path")
  parser.add_argument("--output_filepath", type=str, help="Output filepath")
  args = parser.parse_args()
  main(args)
