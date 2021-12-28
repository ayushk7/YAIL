import sys, os, pathlib
import lark
# import sys

from EmojiInterpreter import EmojiLangInterpeter



if __name__ == "__main__":
    file, parser = None, None
    try:
        file = open('./emojilang.lark', "r")
    except:
        print("STATUS:error in opening the file")
        sys.exit()

    parser = lark.Lark(file, start="stmt")
    print("STATUS:Parser Generated Succesfully")
    print('-----------------------------------------------------------------------------')

    testFileNames = os.listdir('./tests')
    for filName in testFileNames:
        text = None
        try:
            if filName.endswith(".emo"):
                text = pathlib.Path(f"./tests/{filName}").read_text()
        except:
            print(f"STATUS:error in reading the file f /tests/{filName}")
            sys.exit()
        text += '\n'
        tree = None
        tree = parser.parse(text)
        print(f"STATUS:{filName} Parsed Successfully")
        print(tree.pretty())
        runner = EmojiLangInterpeter(tree)
        runner.start()
        print(f"STATUS:{filName} ran without any interrupt")
        print('-----------------------------------------------------------------------------')