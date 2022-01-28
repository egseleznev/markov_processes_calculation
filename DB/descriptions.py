from sqlalchemy import Column, String, Integer
from DB.database import base

class descriptions(base):
        __tablename__ = 'descriptions'
        id = Column(Integer, primary_key=True, autoincrement=True)
        state_number = Column(Integer)
        description = Column(String)

        def __init__(self, id: int, state_number: int, description: str):
            self.id=id
            self.state_number = state_number
            self.description = description

        def __repr__(self):
            info: str = f'{self.state_number}~~{self.description}'
            return info