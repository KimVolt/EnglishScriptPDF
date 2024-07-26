class ChatScript:
    def __init__(self):
        self.name = {}
        self.script = {}
        
    def addName(self, name):
        for key in name:
            if key not in self.name:
                self.name[key] = name[key]
                self.script[key] = []
            else:
                raise Exception(f"[ERROR] Name {key} already exists")
    
    def addScript(self, script):
        for key, value in script.items():
            if key not in self.script:
                self.script[key].append(value)
            else:
                raise Exception(f"[ERROR] Script {key} already exists")
    
    def getScript(self, name):
        return self.script[name]
    
    