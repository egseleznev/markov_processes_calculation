from DB.database import session,db_name, engine
from DB.transitions import *
from sqlalchemy import insert, select, delete
import os
import DB

class DBFunctions():

        def start(self):
            db_is_created = os.path.exists(db_name)
            if not db_is_created:
                DB.database.create_db()


        def insert(self, origin: str, transition: str, weight:str):
            conn = engine.connect()
            ins = insert(transitions).values(origin_state= origin, transition_state= transition, transition_weight= weight)
            conn.execute(ins)

        def select(self):
            result=list([])
            Session =session()
            for row in Session.query(transitions):
                list.append(result,row)
            return result

        def delete(self):
            conn=engine.connect()
            Session =session()
            dell = delete(transitions).where(transitions.id == Session.query(transitions).count())
            conn.execute(dell)

        def rowcount(self):
            Session = session()
            return Session.query(transitions).count()
