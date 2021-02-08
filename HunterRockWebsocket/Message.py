

class Message:

    def __init__(self, raw_data):
        split = [d for d in raw_data.split(" :")]

        self.full_message = raw_data
        self.tags = {}
        self.command = None
        self.user = None
        self.type = None
        self.params = None
        self.channel = None
        self.message = None

        if split[0][0] == "@":
            self.parse_tags(split)

        self.command = split.pop(0).replace(":", "")

        if self.command.startswith(("PING", "PONG")):
            self.type = self.command[:4]
            return

        self.parse_user(self.command)
        self.parse_type(self.command)
        self.parse_params(self.command, self.type)
        self.parse_channel(self.params)

        self.parse_message(split)

    def parse_tags(self, split):
        for fact in split.pop(0)[1:].split(";"):
            key, data = fact.split("=")
            self.tags[key] = data if len(data) > 0 else ""
            #TODO Consider "" vs None

    def parse_user(self, command):
        if not command.startswith(("jtv ", "tmi.twitch.tv ")):
            self.user = command.split("tmi.twitch.tv")[0].split("!")[0]

    def parse_type(self, command):
        self.type = command.split(" ")[1] if "CAP * ACK" not in command else "CAP * ACK"

    def parse_params(self, command, type):
        params = command[command.index(type) + len(type) + 1:]
        self.params = params if len(params) > 0 else ""
        #TODO Consider None vs ""

    def parse_channel(self, params):
        if self.params != None:
            chan_index = self.get_index(params, "#")
            if chan_index != None:
                self.channel = params[chan_index + 1: self.get_index(params, " ", chan_index)]

    def get_index(self, string, substring, start=0):
        try:
            return string.index(substring, start)
        except ValueError:
            return None

    def parse_message(self, split):
        #TODO Consider None vs ""

        if len(split) > 0:
            message = " :".join(split)
            if ord(message[0]) == 1 and message[1:7] == "ACTION":
                message = "/me" + message[7:-1]
            self.message = message
        else:
            self.message = ""

    def __str__(self):
        return (f"user: {self.user}\n\t\t" +
                f"channel: {self.channel}\n\t" +
            f"message: {self.message}\n")
