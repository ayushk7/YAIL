import sys
import lark
# import sys

from EmojiInterpreter import EmojiLangInterpeter



if __name__ == "__main__":
    file = None
    try:
        file = open('./emojilang.lark', "r")
    except:
        print("error in opening the file")
        sys.exit()
    parser = lark.Lark(file, start="stmt")
    text = '''
        a=3
           b=4
           c=a+b
    
    '''
    # text += '\n'
    tree = parser.parse(text)
    print(tree.pretty())
    i = EmojiLangInterpeter(tree)
    i.start()
    # a = 1