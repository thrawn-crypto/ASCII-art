import sys, random, argparse
import numpy as np
import math

from PIL import Image

#grayscale level values from:
# http://paulbourke.net/dataformats/asciiart

#70 levels of grayscale
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray scale
gscale2 = '@%#*+=-:. '

def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale values
    """
    #get image as numpy array
    im = np.array(image)
    #get the dimensions
    w,h = im.shape
    # get the average
    return np.average(im.reshape(w*h))

def covertImageToAscii(fileName, cols, scale, moreLevels):
    """
    Given Image and demensions (row, cols), returns an m*n list of images
    """
    #declare globals
    global gscale1, gscale2
    #open image and covert to grayscale
    image = Image.open(fileName).convert('L')
    #store the image dimensions
    W, H = image.size[0], image.size[1]
    print("input image dims: %d x %d" % (W, H))
    #compute tile width
    w = W/cols
    #compute tile height based on the aspext ratio and scale of the font
    h = w/scale
    # compute number of rows to use in the final grid
    rows = int(H/h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    #check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # an ASCII image is a list of character strings
    aimg = []
    #generate the list of tile dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        #correct the last tile
        if j == rows-1:
            y2 = H
        # append an empty string
        aimg.append("")
        for i in range(cols):
            #crop the image to fit the tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
            #correct the last tile
            if i == cols-1:
                x2 = W
            # crop the image to extract the tile into another Image object
            img = image.crop((x1, y1, x2, y2))
            # get the acerage luminance
            avg = int(getAverageL(img))
            # look up the ASCII character for grayscale value (avg)
            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]
            #append the ASCII character to the string
            aimg[j] += gsval
    #return text image
    return aimg
#main function
def main():
    #create parser
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add expected Arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--moreLevels', dest='moreLevels', action='store_true')

    # parse Arguments
    args = parser.parse_args()

    imgFile = args.imgFile
    #set ouput file
    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile
    #set scale default as 0.43, which suits a courier font
    scale = 0.43
    if args.scale:
        scale = float(args.scale)
    #set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)
    print('generating ASCII art...')
    #convert image to ASCII text
    aimg = covertImageToAscii(imgFile, cols, scale, args.moreLevels)

    #open a new text file
    f = open(outFile, 'w')
    #write each string in the list to the new file
    for row in aimg:
        f.write(row + '\n')
    # clean up
    f.close()
    print("ASCII art written to %s" % outFile)
#call main
if __name__ == '__main__':
    main()
