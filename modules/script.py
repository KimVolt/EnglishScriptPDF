class ChatScript:
    def __init__(self):
        self.topic = ""
        self.script = {}
        self.idx = 0

    def set_topic(self, topic):
        self.topic = topic

    def add_script(self, talker, message):
        if talker not in self.script:
            self.script[talker] = []
                   
        self.script[talker].append((self.idx, message))
        self.idx += 1

    def add_name(self, talkers: list):
        for talker in talkers:
            if talker not in self.script:
                self.script[talker] = []

    def get_script(self, talker):
        return self.script[talker]
    
    def get_talker(self):
        return list(self.script.keys())
