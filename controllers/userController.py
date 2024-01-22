from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.employee import employee
from models.user import user

class userController:

        def get_users(self):
            engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()

            users = session.query(user).all()
            return users

        def get_user_by_id(self, id):
            engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()

            usr = session.query(user).filter_by(id=id).first()
            return usr

        def get_user_by_username(self, username):
            engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()

            usr = session.query(user).filter_by(username=username).first()
            return usr

        def get_user_by_username_and_password(self, username, password):
            engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()

            users = session.query(user, employee).join(employee, user.employeeID == employee.employeeID).filter(user.username == username, user.password == password).first()
            # users = session.query(user).filter_by(username=username, password=password).first()
            return users