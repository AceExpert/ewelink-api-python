class UnboundRegion(Exception):
    region: str
    __slots__ = ('region',)
    def __init__(self, region: str):
        self.region = region
        super().__init__(f"{region} does not exist.")

    def __repr__(self) -> str:
        return f"<UnboundRegion {self.region} does not exist>"

    def __str__(self) -> str:
        return f"{self.region} does not exist."