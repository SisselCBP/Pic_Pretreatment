import sys, getopt, os
from PIL import Image

helpmsg = "用法: check.py -i <inputfile> | -a\n" \
        "    -i|--ifile 输入文件名\n" \
        "    -a|--all   遍历当前文件夹下所有png文件，检查是否有问题\n" \
        "    -h|--help  帮助信息"

after_color = ((0,0,0), (255,255,255),(150,150,150),(255, 0, 0),(0, 255, 0),(0, 0, 255),(0, 128, 255),(255, 0, 255),(0, 255, 255),(128, 0, 255),(255, 255, 0),(128, 0, 0),(0, 0, 128),(0, 128, 0),(128, 128, 0),(128, 0, 128),(0, 128, 128),(128, 255, 0),(255, 128, 0),(255, 0, 128),(0, 255, 128),(128, 128, 255),(128, 255, 128))

def main(argv):
    inputfile = ''
    level = 0
    try:
        opts, args = getopt.getopt(argv,"ahsi:",["ifile="])
    except getopt.GetoptError:
        print('pre.py -i <inputfile> | -a')
        sys.exit(2)
    if len(opts) == 0:
        print('pre.py -i <inputfile> | -a')
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(helpmsg)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = [arg]
        elif opt in ("-a", "--all"):
            inputfile = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.png']
        elif opt in ("-s", "--self"):
            inputfile = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.png' and ('mask' in os.path.splitext(x)[0])]
            outputfile = [x.replace("mask", "src") for x in inputfile]

    for op in range(len(inputfile)):
        filein = inputfile[op]
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
                color = im.getpixel((i, j))
                if color[:-1] not in after_color :
                    print(filein + '\t有问题,坐标为('+ str(i) + ',' + str(j) + ')')

if __name__ == "__main__":
    main(sys.argv[1:])



