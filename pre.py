import sys, getopt, os
from PIL import Image

helpmsg = "用法: pre.py [[-i <inputfile> [-o <outputfile>]] | [-a]] [-l <level>]\n" \
        "    -i|--ifile 输入文件名\n" \
        "    -o|--ofile 指定输出文件名，默认为pre-*.png\n" \
        "    -a|--all   遍历当前文件夹下所有png文件，并进行预处理，输出文件名均为默认名称\n" \
        "    -l|--level [0|1]指定颜色替换强度，默认为0，复杂计算替换为1\n" \
        "    -h|--help  帮助信息"

after_color = ((255, 0, 0),(0, 255, 0),(0, 0, 255),(0, 128, 255),(255, 0, 255),(0, 255, 255),(128, 0, 255),(255, 255, 0),(128, 0, 0),(0, 0, 128),(0, 128, 0),(128, 128, 0),(128, 0, 128),(0, 128, 128),(128, 255, 0),(255, 128, 0),(255, 0, 128),(0, 255, 128),(128, 128, 255),(128, 255, 128))

def main(argv):
    inputfile = ''
    outputfile = ''
    level = 0
    try:
        opts, args = getopt.getopt(argv,"ahsi:o:l:",["ifile=","ofile=","level="])
    except getopt.GetoptError:
        print('pre.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    if len(opts) == 0:
        print('pre.py -i <inputfile> -o <outputfile>')
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(helpmsg)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = [arg]
        elif opt in ("-o", "--ofile"):
            outputfile = [arg]
        elif opt in ("-a", "--all"):
            inputfile = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.png']
        elif opt in ("-s", "--self"):
            inputfile = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.png' and ('mask' in os.path.splitext(x)[0])]
            outputfile = [x.replace("mask", "src") for x in inputfile]
        elif opt in ("-l", "--level"):
            if arg.isdigit():
                level = int(arg)
            else:
                print("参数错误！")
                sys.exit()

    if len(outputfile) == 0:
        outputfile = [os.path.join(os.path.abspath('.'), "pre-"+os.path.split(x)[1]) for x in inputfile]

    for op in range(len(inputfile)):
        filein = inputfile[op]
        fileout = outputfile[op]
        try:
            im = Image.open(filein)
            im = im.convert("RGBA")
        except:
            print('未找到该文件!')
            sys.exit()
        width = im.size[0]
        length = im.size[1]
        om = Image.new('RGBA', im.size)
        for i in range(width):
            for j in range(length):
                color = check_color(im.getpixel((i, j)))
                om.putpixel([i,j], tuple(color))
        for terns in range(level+1):
            for i in range(width):
                for j in range(length):
                    color = om.getpixel((i, j))[:3]
                    if not (color[0] == color[1] and color[1] == color[2] and color[2] == color[0]):
                        if color not in after_color:
                            near_color = []
                            near_color_old = []
                            near_color.append(om.getpixel((i-1, j))[:3])
                            near_color.append(om.getpixel((i+1, j))[:3])
                            near_color.append(om.getpixel((i, j-1))[:3])
                            near_color.append(om.getpixel((i, j+1))[:3])
                            near_color_old.append(im.getpixel((i-1, j))[:3])
                            near_color_old.append(im.getpixel((i+1, j))[:3])
                            near_color_old.append(im.getpixel((i, j-1))[:3])
                            near_color_old.append(im.getpixel((i, j+1))[:3])
                            flag = 999
                            for k in range(len(near_color)):
                                if near_color[k] in after_color:
                                    check = abs(color[0]-near_color_old[k][0])+abs(color[1]-near_color_old[k][1])+abs(color[2]-near_color_old[k][2])
                                    if check < flag:
                                        om.putpixel([i, j], near_color[k])
                                        flag = check

        om.save(fileout, quality=100)

def check_color(rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]
    if r == 0 and g == 159 and b == 48:
        return [255, 0, 0]
    elif r == 177 and g == 135 and b == 60:
        return [0, 255, 0]
    elif r == 177 and g == 63 and b == 90:
        return [0, 0, 255]
    elif r == 255 and g == 39 and b == 108:
        return [0, 128, 255]
    elif r == 255 and g == 111 and b == 72:
        return [255, 0, 255]
    elif r == 0 and g == 15 and b == 120:
        return [0, 255, 255]
    elif r == 177 and g == 246 and b == 132:
        return [128, 0, 255]
    elif r == 0 and g == 87 and b == 84 :
        return [255, 255, 0]
    elif r == 0 and g == 198 and b == 156 :
        return [128, 0, 0]
    elif r == 255 and g == 222 and b == 144 :
        return [0, 0, 128]
    elif r == 0 and g == 126 and b == 192:
        return [0, 128, 0]
    elif r == 255 and g == 150 and b == 180:
        return [128, 128, 0]
    elif r == 177 and g == 174 and b == 168:
        return [128, 0, 128]
    elif r == 177 and g == 102 and b == 204:
        return [0, 128, 128]
    elif r == 255 and g == 78 and b == 216:
        return [128, 255, 0]
    elif r == 255 and g == 0 and b == 0:
        return [255, 128, 0]
    elif r == 0 and g == 231 and b == 12:
        return [255, 0, 128]
    elif r == 177 and g == 207 and b == 24:
        return [0, 255, 128]
    elif r == 255 and g == 183 and b == 36:
        return [128, 128, 255]
    elif r == 0 and g == 54 and b == 228:
        return [128, 255, 128]
    else:
        return [r, g, b]

if __name__ == "__main__":
    main(sys.argv[1:])



