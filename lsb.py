from PIL import Image
import os
     binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message
 
 
def encode_lsb(image_path, message):
    img = Image.open(image_path)
    width, height = img.size
    binary_message = message_to_bin(message)
    binary_message += '1111111111111110'  
 
    if len(binary_message) > width * height * 3:
        raise Exception("Message too long to encode in the given image")
 
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & 0b11111110 | int(binary_message[data_index])
                    data_index += 1
            img.putpixel((x, y), tuple(pixel))
 
 
    output_directory = os.path.dirname(image_path)
 
    output_image_path = os.path.join(output_directory, "encoded.png")
 
    img.save(output_image_path)
    print("Message encoded successfully. Output image saved as:", output_image_path)
 
def decode_lsb(image_path):
    img = Image.open(image_path)
    width, height = img.size
    binary_message = ''
 
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                binary_message += str(pixel[i] & 1)
 
    sentinel_index = binary_message.find('1111111111111110')
    if sentinel_index == -1:
        raise Exception("No message found in the image")
 
    binary_message = binary_message[:sentinel_index]
 
    message = ''
    for i in range(0, len(binary_message), 8):
        message += chr(int(binary_message[i:i+8], 2))
    print("Decoded message:", message)
 
def main():
    image_path = input("Enter the path to the image: ")
    while not os.path.isfile(image_path):
        print("Invalid image path. Please try again.")
        image_path = input("Enter the path to the image: ")
 
    while True:
        print("\nLSB Steganography Menu:")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Exit")
        choice = input("Enter your choice: ")
 
        if choice == '1':
            message = input("Enter the message to encode: ")
            encode_lsb(image_path, message)
        elif choice == '2':
            decode_lsb(image_path)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")
 
if __name__ == "__main__":
    main()
