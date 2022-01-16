from check_appointment import CheckAppointment
import datetime
import time

while datetime.datetime.now().hour < 10:
    test = CheckAppointment()
    test.setup_method()
    test.check_if_appointment_available()
    time.sleep(40)
