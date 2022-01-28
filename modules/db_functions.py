from DB.database import session,db_name, engine
from DB.transitions import *
from DB.descriptions import *
from sqlalchemy import insert, select, delete
import os
import DB

class DBFunctions():

        def start(self):
            db_is_created = os.path.exists(db_name)
            if not db_is_created:
                DB.database.create_db()


        def inserttransition(self, origin: str, transition: str, weight:str):
            conn = engine.connect()
            ins = insert(transitions).values(origin_state= origin, transition_state= transition,
                                                            transition_weight= weight)
            conn.execute(ins)

        def selecttransition(self):
            result=list([])
            Session =session()
            for row in Session.query(transitions):
                list.append(result,row)
            return result

        def deletetransition(self):
            conn=engine.connect()
            Session =session()
            dell = delete(transitions).where(transitions.id == Session.query(transitions).count())
            conn.execute(dell)

        def insertdescription(self, state: int, desc:str):
            conn = engine.connect()
            ins = insert(descriptions).values(state_number=state, description=desc)
            conn.execute(ins)

        def selectdescription(self):
            result = list([])
            Session = session()
            for row in Session.query(descriptions):
                list.append(result, row)
            return result

        def deletedescription(self):
            conn = engine.connect()
            Session = session()
            dell = delete(descriptions).where(descriptions.id == Session.query(descriptions).count())
            conn.execute(dell)
