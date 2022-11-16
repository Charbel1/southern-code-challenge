from datetime import datetime


class ValidationDate():
    def parse_formate_date(self,date:datetime):
        return datetime.strptime(date, '%m-%d-%Y').date()

    def validate_change_greater(self,start:datetime,end:datetime):
        return start > end
