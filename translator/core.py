import argparse

class Base:
    def __init__(self):
        pass

    def stdin(self):
        parser = argparse.ArgumentParser(description="Translate...")
        parser.add_argument("word",)
        args = parser.parse_args()
        return args.word 

    def request(self):
        stdin = self.stdin()
        print(stdin)
    
    def response(self):
        pass
    
    def stdout(self):
        pass
    
base = Base()
base.request()
