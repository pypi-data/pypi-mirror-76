class NotConnectedError(ValueError):
    def __init__(self, from_key, to_key):
        super().__init__(
            "Adding link %s -- %s would create a cycle" % (from_key, to_key)
        )
        self.from_key = from_key
        self.to_key = to_key
