class ServerError(Exception):
    def __init__(self, fault_code):
        super().__init__("ServerError: {}".format(fault_code))
        self.fault_code = fault_code
