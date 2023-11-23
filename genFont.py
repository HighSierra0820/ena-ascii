from PIL import Image,ImageFont,ImageDraw

fontPicPath="assets/fontpic/"
fontFilePath="assets/fontfile/"

fontFileName=f"{fontFilePath}iosevka.ttf"
fontSize=16

font=ImageFont.truetype(fontFileName,fontSize)
fontName='_'.join((font.getname()))

glyphHeight=sum(font.getmetrics())
glyphWidth=font.getbbox(' ')[2]

charset=list(chr(i) for i in range(32,127)) # printable ASCII

if __name__=="__main__":
    for ch in charset:
        ordOfCh=ord(ch)
        saveName=f'assets/fontpic/{fontName}_{hex(ordOfCh)[2:]:2s}.png'
        newImage=Image.new(mode='RGB',size=(glyphWidth,glyphHeight))
        newImageDraw=ImageDraw.Draw(newImage)
        newImageDraw.text((0,0),ch,font=font)
        newImage.save(saveName)