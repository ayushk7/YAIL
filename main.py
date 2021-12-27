import lark
import sys





if __name__ == "__main__":
    file = None
    try:
        file = open('./emojilang.lark', "r")
    except:
        print("error in opening the file")
        sys.exit()
    parser = lark.Lark(file, start="stmt")
    text = '''
        for (a=2; a <5; a=a+1){
            print("hi")
        }
    '''
    text += '\n'
    tree = parser.parse(text)
    print(tree.pretty())