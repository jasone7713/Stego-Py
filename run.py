import utils
import cv2
import augment
import image_reader as reader

#   get a message from the reader either in the form of a txt file path or a plain string
#   get the filepath of an image from the reader
#   get settings from the reader:
#       -do they want to add noise to their picture?
#       -which channel mode would they like to use?
#   get output file name and path from user, if none provided generate a random name and pit in bin directory

def encode():
    # GET MSG TO ENCODE
    print('Input a message that you would like to encode, or just click enter to choose a .txt file. Press q to quit')
    ui = input()
    if utils.check_input(ui):
        return False
    msg = utils.get_msg(ui)

    # GET IMG TO ENCODE
    print('Chose the image that you want to encode the message into')
    img = cv2.imread(utils.read_file_path())
    if img is None:
        print('Error reading the image you chose')
        return True

    # CHECK PARAMETERS
    print('Do you want to add Gaussian noise to your image (yes/no)')
    ui = input()
    if 'YES' in ui.upper():
        img = augment.add_gaussian_noise(img, 5, 5)

    # OUTPUT FILENAME
    print('Enter the name of your output file. Press q to quit')
    outfile = utils.create_new_file_path()
        
    # DO THE ENCODING
    cv2.imwrite(outfile, reader.embed(img, msg, 0))

def decode_img():
     # GET IMG TO DECODE
    print('Chose the image that you want to decode')
    img = cv2.imread(utils.read_file_path())
    if img is None:
        print('Error reading the image you chose')
        return True
    msg = reader.decode(img)
    print(msg)
    input()

def run():
    while True:

        print('Would you like to encode or decode an image? (0 for encode, 1 for decode)')
        ui = input()

        if '0' in ui:
            if encode(): 
                break       
        elif '1' in ui:
            decode_img()

        
if __name__ == '__main__':
    run()