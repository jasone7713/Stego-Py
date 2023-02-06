import cv2
import math
import numpy as np

#CONSTANTS
DELIMETER = '||end||'
OFFSET_INDEX = 0
CHANNEL_INDEX = 2

def read_image(filename):
    img = cv2.imread(filename, -1)
    return img

def write_image(filename, img):
    cv2.imwrite(filename, img)

#given any number round it down to the closest (lower-bound) power of 2
def round_down_to_power_of_2(number):
    root = int(math.sqrt(number))
    if root ** 2 == number:
        return number
    while root ** 2 > number:
        root -= 1
    return root ** 2 if root <= 255 else 255

def calculate_offset(message_length, rows, cols, first_pixel):
    #total amount of pixels in image minus the first row
    num_pixels = (rows - 1) * cols

    #Add +1 to message length for the information pixel and +5 for the \end\ DELIMETER
    offset = int(num_pixels / (message_length + 6))

    #round offset down to the closest number thats sqrt(2) is an integer
    return round_down_to_power_of_2(offset)

#given a pixel and a character, convert the desired channels pixel value to the ASCII version of that character
def convert_pixel(pixel, ch, channel):
    pixel[channel] = ord(ch)
    return pixel

def embed_offset(pixel, offset):
    offset = int(math.sqrt(offset))
    pixel[OFFSET_INDEX] = offset
    return pixel

def average_neighbor_value(img, x, y):
    avg = np.array([0, 0, 0], dtype=np.float64)
    count = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if x + i >= 0 and x + i < img.shape[0] and y + j >= 0 and y + j < img.shape[1] and (i != 0 or j != 0):
                avg += img[x + i, y + j]
                count += 1
    avg = avg / float(count)
    return np.argmin(avg)

#given a pixel, find the color channel by taking the channel that has the minimum avg influence in neighboring 8 pixels
def calculate_channel(img, x, y):
    channel = average_neighbor_value(img, x, y)
    channel = 0
    return channel

def update_channel(channel):
    return (channel + 1) % 2

def embed(img, msg, channel = 0):
    
    rows,cols,_ = img.shape
    reference_img = img

    #the DELIMETER is a safety measure to mark when the end of the msg is reached
    msg += DELIMETER

    pixel = img[0, 0]
    offset = calculate_offset(len(msg), rows, cols, pixel)

    #embed the offset to store in pixel
    embed_offset(pixel, offset)

    #this will save the channel being used for pixel changes
    pixel[CHANNEL_INDEX] = channel

    #save the modified pixel in the image
    img[0, 0] = pixel

    counter = 0
    index_in_msg = 0

    print('The offset used to embed: ', offset)
    #iterate through every pixel in image
    for i in range(1, rows): #skip first row -> that's where I am storing information
        for j in range(cols):

            #change the pixel value on every nth pixel
            if counter == offset:
                k = img[i,j]

                #check bounds of message
                if index_in_msg >= len(msg):
                    break
                img[i,j] = convert_pixel(k, msg[index_in_msg], calculate_channel(reference_img, j, i))
                index_in_msg += 1
                counter = 0
            else:
                counter += 1

    return img

def decode_pixel(pixel, channel):
    return chr(pixel[channel])

def remove_DELIMETER(msg, DELIMETER):
    return msg[:-len(DELIMETER)]

def read_offset(pixel):
    offset = pixel[OFFSET_INDEX]
    return offset ** 2

def decode(img):
    rows,cols,_ = img.shape
    reference_img = img

    pixel = img[0, 0]
    offset = read_offset(pixel)
    channel = pixel[CHANNEL_INDEX]
    counter = 0
    msg = ''
    terminated = False

    print('The offset used to decode: ', offset)

    #iterate through every pixel in image
    for i in range(1, rows):

        #break when end of message reached
        if terminated:
                break

        for j in range(cols):
            #change the pixel value on every nth pixel
            if counter == offset:
                k = img[i,j]
                msg += decode_pixel(k, calculate_channel(reference_img, j, i))
                if DELIMETER in msg:
                    return remove_DELIMETER(msg, DELIMETER)
                counter = 0
                channel = update_channel(channel)
            else:
                counter += 1

    print('Error: the end of the image was reached before message terminated')
    return ''