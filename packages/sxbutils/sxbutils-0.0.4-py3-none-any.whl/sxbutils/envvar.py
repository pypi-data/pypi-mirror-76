class envvar:
    def __init__(self, name, required, example):
        self.name=name
        self.required=required
        self.example=example

    def tostr(self):
        tostr="name="+self.name+" required="+str(self.required)+" example="+self.example
        print("name="+self.name)
        print("required="+str(self.required))
        print("example="+self.example)
        return tostr

