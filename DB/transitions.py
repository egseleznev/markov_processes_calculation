from sqlalchemy import Column, String, Integer
from DB.database import base

class transitions(base):
        __tablename__ = 'transitions'
        id = Column(Integer, primary_key=True, autoincrement=True)
        origin_state = Column(String)
        transition_state = Column(String)
        transition_weight = Column(String)

        def __init__(self, id: int, origin: str, transition: str, weight:str):
            self.id=id
            self.origin_state = origin
            self.transition_state = transition
            self.transition_weight = weight

        def __repr__(self):
            info: str = f'{self.origin_state} {self.transition_state} {self.transition_weight}'
            return info
