from datetime import datetime
from ago import human

class FancyTime():
    def __init__(self, dt: datetime):
        self.dt = dt

    @property
    def human(self):
        return human(self.dt)

    @property
    def iso(self):
        return self.dt.isoformat(" ")
