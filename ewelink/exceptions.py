class RegionDoesNotExist(Exception):
    def __init__(self, region : str ,message=" is not a valid region."):
        self.region = region
        self.message = message
        super().__init__(message)
    def __str__(self):
        return f"{self.region}{self.message}"
