class DataStreamHandler:
    def __init__(self):
        self.data_streams = []

    def add_stream(self, stream):
        self.data_streams.append(stream)

    def run(self):
        while True:
            for stream in self.data_streams:
                pass


