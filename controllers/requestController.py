from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.employee import employee
from models.request import request

class requestController:

    def get_request_and_employee_data(self):
        engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        employeereqeuests = session.query(request, employee).join(employee, request.employeeID == employee.employeeID).all()
        return employeereqeuests

    def get_requests(self):
        engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        requests = session.query(request).all()
        return requests

    def get_request_by_id(self, id):
        engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        req = session.query(request).filter_by(id=id).first()
        return req

    def get_request_by_employee_id(self, employee_id):
        engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        req = session.query(request).filter_by(employee_id=employee_id).first()
        return req

    def get_request_by_status(self, status):
        engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        req = session.query(request).filter_by(status=status).all()
        return req

    def update_request(self, id, status):
        engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        req = session.query(request).filter_by(id=id).first()
        req.status = status
        session.commit()
        return req

    def delete_request(self, id):
        engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        req = session.query(request).filter_by(id=id).first()
        session.delete(req)
        session.commit()
        return req

    def create_request(self, employee_id, start_date, end_date, leaveType, reason, status):
        engine = create_engine('sqlite:///HRLeaveRequest.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        if start_date > end_date:
            return "Error: Start date must be before end date."
        current_year = datetime.now().year
        existing_requests = session.query(request).filter_by(employeeID=employee_id).filter(
            request.startLeaveDate.year == current_year).all()
        total_days = sum((req.endLeaveDate - req.startLeaveDate).days + 1 for req in existing_requests)
        new_request_days = (end_date - start_date).days + 1
        if total_days + new_request_days > 10:
            return "Error: Total leave days in a year cannot exceed 10 days."
        for existing_requests in existing_requests:
            if start_date <= existing_requests.endLeaveDate and end_date >= existing_requests.startLeaveDate:
                return "Error: New request overlaps with an existing request."

        new_request = request(requestReason=reason, startLeaveDate=start_date, endLeaveDate=end_date, leaveType=leaveType, employeeID=employee_id,requestStatus=status)
        session.add(new_request)
        session.commit()
        return new_request