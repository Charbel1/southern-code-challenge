from datetime import datetime


class DateValidation():
    def parse_formate_date(self,date:datetime):
        return datetime.strptime(date, '%m-%d-%Y').date()

    def greater_date_validat_change(self, start:datetime, end:datetime):
        return start > end
