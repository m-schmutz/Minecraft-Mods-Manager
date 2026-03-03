from dataclasses import dataclass
from .schemas import ModsTable


@dataclass
class ModInsert:
    name: str
    description: str
    version:str
    filename: str
    filehash: str
    link: str
    type: str
    role: str

    def __init__(self, str_values: dict[str, str], filename: str, filehash:str):
        self.name = str_values[ModsTable.NAME]
        self.description = str_values[ModsTable.DESCRIPTION]
        self.version = str_values[ModsTable.VERSION]
        self.filename = filename
        self.filehash = filehash
        self.link = str_values[ModsTable.LINK]
        self.type = str_values[ModsTable.TYPE]
        self.role = str_values[ModsTable.ROLE]





