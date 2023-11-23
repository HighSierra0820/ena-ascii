from sys import argv
from PIL import Image,ImageFont,ImageDraw
from time import localtime, strftime

from genFont import fontName, fontFileName, fontSize, glyphWidth, glyphHeight, charset, fontPicPath, fontFilePath

bias=128

glyphMap={}
for ch in charset:
    ordOfCh=ord(ch)
    fontPicName=f'{fontName}_{hex(ordOfCh)[2:]:2s}.png'
    fontPic=Image.open(fontPicPath+fontPicName)
    fontPic=fontPic.convert("L")
    fontPicData=fontPic.getdata()
    biasedFontPicData=list(map(lambda x: x-bias,fontPicData))
    glyphMap[ch]=biasedFontPicData

if len(argv)<2:
    print("Usage: python genPic.py filename [width]")
    exit(0)

imageName=argv[1]
image=Image.open(imageName)
image=image.convert("L")

width,height=0,0

if len(argv)>=3:
    width=int(argv[2])
    height=int(image.size[1]*width/image.size[0])
else:
    width,height=image.size

width=round(number=width/glyphWidth)*glyphWidth
height=round(height/glyphHeight)*glyphHeight

image=image.resize((width,height))
imageData=image.getdata()
imageMatrix=[[255-bias for i in range(width)] for j in range(height)]
for i in range(len(imageData)):
    imageMatrix[i//width][i%width]=255-imageData[i]-bias

charCountWidth=width//glyphWidth
charCountHeight=height//glyphHeight

charMatrix=[[0 for i in range(charCountWidth)] for j in range(charCountHeight)]

for i in range(charCountHeight):
    if i%5==0:
        print(f"Processing line {i:3d}/{charCountHeight-1:3d}...")
    for j in range(charCountWidth):
        maxScore=-1e10
        maxChar=None
        for ch in glyphMap:
            score=0.0
            for k in range(glyphHeight):
                for l in range(glyphWidth):
                    score+=(glyphMap[ch][k*glyphWidth+l])/128.0*(imageMatrix[i*glyphHeight+k][j*glyphWidth+l])/128.0
            if score>maxScore:
                maxScore=score
                maxChar=ch
        charMatrix[i][j]=maxChar

outputFilename=f"{strftime('%Y%m%d_%H%M%S', localtime())}_{width}x{height}.png"
outputPath="output/"

outputImage=Image.new("L",(width,height))
draw=ImageDraw.Draw(outputImage)
font=ImageFont.truetype(fontFileName,fontSize)

for i in range(len(charMatrix)):
    for j in range(len(charMatrix[i])):
        draw.text((j*glyphWidth,i*glyphHeight),charMatrix[i][j],font=font,fill=255)
outputImage.save(f"{outputPath}{outputFilename}")
print(f"Output file: {outputPath}{outputFilename}")