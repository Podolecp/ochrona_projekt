__author__ = 'Antah'
from database import Base, User, Log
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
sessiondb = DBSession()

#user = sessiondb.query(User).filter(User.username == 'do usuniecia').first()
#admin = User(u'admin',u'admin',u'Kim jestes',u'admin')
#sessiondb.add(admin)
#sessiondb.commit()

#log = Log(u'admin','jakisssss log')
#sessiondb.add(log)
#sessiondb.commit()

for instance in sessiondb.query(Log).filter(Log.username=='admin').order_by(Log.id):
    print instance.username, instance.log