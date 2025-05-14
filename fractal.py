
#Importing the libraries to plot pixels in the canvas
from PIL import Image
import random

#IFS Code Associated with the Fractal to be generated
#[A,B,C,D,E,F,P]
input=[[0.309045,-0.224534,0.224534,0.309000,0.0000,0.0000,0.167],
     [-0.118045,-0.363304,0.363304,-0.118045,0.3090,0.2250,0.167],
     [0.309045,0.224534,-0.224534,0.309045,0.1910,0.5880,0.167],
     [-0.118045,0.363304,-0.363304,-0.118045,0.5000,0.3630,0.167],
     [0.309045,0.224534,-0.224534,0.309045,0.3820,0.0000,0.167],
     [0.309045,-0.224534,0.224534,0.309045,0.6910,-0.2250,0.165]]

# image size on the x-axis and y-axis i.e, number of pixels generated in the image for each axis
x_img = 512
y_img = 512 

#calculating the number of cells in the given data
m = len(input)

# finding the xmin, xmax, ymin, ymax
x = input[0][4]
y = input[0][5] 

#Considering Xmin, Xmax & Ymin, Ymax 
xa = x
xb = x
ya = y
yb = y

#Random iteration will start here 
for k in range(x_img * y_img):
    #An initial random point is chosen using the Random library provided
    p=random.random()
    randsum = 0.0
    for i in range(m):
        randsum += input[i][6]
        if p <= randsum:
            break
    
    #Applying Affine Transforinpution number k to (x,y)
    x0 = x * input[i][0] + y * input[i][1] + input[i][4] 
    y  = x * input[i][2] + y * input[i][3] + input[i][5] 
    x = x0 
    
    if x < xa:
        xa = x
    if x > xb:
        xb = x
    if y < ya:
        ya = y
    if y > yb:
        yb = y

# drawing the fractal 
image = Image.new("L", (x_img, y_img))

x=0.0
y=0.0 

#Similarly like the previous question, we are plotting it by making the pixel value to white
for k in range(x_img * y_img):
    print('iteration:' +str(k))
    p=random.random()
    randsum = 0.0
    for i in range(m):
        randsum += input[i][6]
        if p <= randsum:
            break
    x0 = x * input[i][0] + y * input[i][1] + input[i][4] 
    y  = x * input[i][2] + y * input[i][3] + input[i][5] 
    x = x0 
    jx = int((x - xa) / (xb - xa) * (x_img - 1)) 
    jy = (y_img - 1) - int((y - ya) / (yb - ya) * (y_img - 1))
    image.putpixel((jx, jy), 255) 
    if(k%50000==0):
      image.save("RandomIteration"+str(k)+".png", "PNG")
image.save("RandomIteration Final.png", "PNG")
#Here the fractal is generated after completing 262143 iterations successfully.
#The most awaited Fractal is now saved in the file named: Fractal.jpg 
     