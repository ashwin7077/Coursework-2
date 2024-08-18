from PIL import Image
import sys

class Steganography:
    def __init__(self, image_path=None):
        self.image_path = image_path

    @staticmethod
    def pix_val(image):
        with Image.open(image) as im:
            return list(im.getdata())

    @staticmethod
    def genData(data):
        return [format(ord(i), '08b') for i in data]

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):
            pixels = [value for value in imdata.__next__()[:3] +
                                 imdata.__next__()[:3] +
                                 imdata.__next__()[:3]]

            for j in range(8):
                if (datalist[i][j] == '0' and pixels[j] % 2 != 0):
                    pixels[j] -= 1
                elif (datalist[i][j] == '1' and pixels[j] % 2 == 0):
                    pixels[j] = pixels[j] - 1 if pixels[j] != 0 else pixels[j] + 1

            if i == lendata - 1:
                if pixels[-1] % 2 == 0:
                    pixels[-1] = pixels[-1] - 1 if pixels[-1] != 0 else pixels[-1] + 1
            else:
                if pixels[-1] % 2 != 0:
                    pixels[-1] -= 1

            yield tuple(pixels[:3])
            yield tuple(pixels[3:6])
            yield tuple(pixels[6:9])

    def encode_enc(self, newimg, data):
        w, h = newimg.size
        x, y = 0, 0

        for pixel in self.modPix(self.pix_val(self.image_path), data):
            newimg.putpixel((x, y), pixel)
            x += 1
            if x == w:
                x = 0
                y += 1

    def encode(self):
        try:
            img = input("Enter image name (with extension): ")
            with Image.open(img) as image:
                self.image_path = img
                data = input("Enter message to be encoded: ")
                if len(data) == 0:
                    raise ValueError('Message is empty')

                newimg = image.copy()
                self.encode_enc(newimg, data)

                new_img_name = input("Enter the name of new image (save as .png extension only): ")
                newimg.save(new_img_name, format='PNG')
                print("Image saved successfully.")

        except FileNotFoundError:
            print("Image not found. Try again.")
        except ValueError as ve:
            print(ve)

    def decode(self):
        try:
            pixel_values = self.pix_val(self.image_path)
            data = ''
            imgdata = iter(pixel_values)

            while True:
                pixels = [value for value in imgdata.__next__()[:3] +
                                     imgdata.__next__()[:3] +
                                     imgdata.__next__()[:3]]

                binstr = ''.join('0' if i % 2 == 0 else '1' for i in pixels[:8])
                data += chr(int(binstr, 2))

                if pixels[-1] % 2 != 0:
                    return data

        except FileNotFoundError:
            print("Image not found. Try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    stego = Steganography()
    while True:
        a = input("Welcome to stegno script\n1. Encode\n2. Decode\nEnter the option number: ")
        if a == '1':
            stego.encode()
        elif a == '2':
            stego.image_path = input("Enter image name (with extension) for decoding: ")
            print("Decoded Word: " + stego.decode())
        else:
            print('Invalid option. Try again.')
        
        answer = input('Do you want to try another time? (y or n): ')
        if answer.lower() != 'y':
            print('Thank you for trying out this tool. Exiting...')
            sys.exit()

if __name__ == "__main__":
    main()
