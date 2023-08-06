import fire

from simplecmr import query

class CLI(query.Query):
    def __init__(self,*args,**kwargs):
        super(CLI, self).__init__(*args,**kwargs)
        return

    def fetch



def main():
    fire.Fire(CLI)
