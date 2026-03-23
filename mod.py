from dataclasses import dataclass



@dataclass
class Dependancy:
    idStr: str
    depType: str
    versionRange: str
    side: str





@dataclass
class Mod:
    idStr: str
    version: str
    name: str
    url: str
    description: str
