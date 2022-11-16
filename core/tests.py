
import os
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reservations.settings")
import django
django.setup()
from core.models import PricingRule
from core.models import Property

from core.views.calculate_booking import UtilityCalculateBooking


# Create your tests here.
from unittest import TestCase


class TestSetBookingView(TestCase):
    def test_case_1(self):
        pro = Property()
        pro.name = "test"
        pro.base_price = 10
        pro.save()
        pricing_rule = PricingRule()
        pricing_rule.property = pro
        pricing_rule.price_modifier = -10
        pricing_rule.min_stay_length = 10
        pricing_rule.save()
        utility = UtilityCalculateBooking()

        date_start  = "11-1-2022"
        date_end    = "11-10-2022"
        final_value = utility.calcutate_final_price_booking(pro.id,date_start,date_end)
        pro.delete()
        pricing_rule.delete()

        self.assertEqual(90,final_value)

    def test_case_2(self):
        pro = Property()
        pro.name = "test"
        pro.base_price = 10
        pro.save()
        pricing_rule = PricingRule()
        pricing_rule.property = pro
        pricing_rule.price_modifier = -10
        pricing_rule.min_stay_length = 10
        pricing_rule.save()

        pricing_rule2 = PricingRule()
        pricing_rule2.property = pro
        pricing_rule2.price_modifier = -20
        pricing_rule2.min_stay_length = 30
        pricing_rule2.save()

        utility = UtilityCalculateBooking()

        date_start = "11-1-2022"
        date_end = "11-10-2022"
        final_value = utility.calcutate_final_price_booking(pro.id, date_start, date_end)
        pro.delete()
        pricing_rule.delete()
        pricing_rule2.delete()

        self.assertEqual(90, final_value)

    def test_case_3(self):
        pro = Property()
        pro.name = "test"
        pro.base_price = 10
        pro.save()
        pricing_rule = PricingRule()
        pricing_rule.property = pro
        pricing_rule.price_modifier = -10
        pricing_rule.min_stay_length = 10
        pricing_rule.save()

        pricing_rule2 = PricingRule()
        pricing_rule2.property = pro
        pricing_rule2.specific_day = datetime.strptime("11-1-2022", '%m-%d-%Y').date()
        pricing_rule2.fixed_price = 20
        pricing_rule2.save()


        utility = UtilityCalculateBooking()

        date_start = "11-1-2022"
        date_end = "11-10-2022"
        final_value = utility.calcutate_final_price_booking(pro.id, date_start, date_end)
        pro.delete()
        pricing_rule.delete()
        pricing_rule2.delete()

        self.assertEqual(101, final_value)

    def test_case_4(self):
        pro = Property()
        pro.name = "test"
        pro.base_price = 10
        pro.save()
        pricing_rule = PricingRule()
        pricing_rule.property = pro
        pricing_rule.price_modifier = -10
        pricing_rule.min_stay_length = 10
        pricing_rule.save()

        pricing_rule2 = PricingRule()
        pricing_rule2.property = pro
        pricing_rule2.specific_day = datetime.strptime("11-1-2022", '%m-%d-%Y').date()
        pricing_rule2.fixed_price = 20
        pricing_rule2.save()

        pricing_rule2 = PricingRule()
        pricing_rule2.property = pro
        pricing_rule2.specific_day = datetime.strptime("11-2-2022", '%m-%d-%Y').date()
        pricing_rule2.min_stay_length = 10
        pricing_rule2.fixed_price = 20
        pricing_rule2.save()

        utility = UtilityCalculateBooking()

        date_start = "11-1-2022"
        date_end = "11-10-2022"
        final_value = utility.calcutate_final_price_booking(pro.id, date_start, date_end)
        pro.delete()
        pricing_rule.delete()
        pricing_rule2.delete()

        self.assertEqual(112, final_value)

    def test_case_5(self):
        pro = Property()
        pro.name = "test"
        pro.base_price = 10
        pro.save()
        pricing_rule = PricingRule()
        pricing_rule.property = pro
        pricing_rule.price_modifier = -10
        pricing_rule.min_stay_length = 10
        pricing_rule.save()

        pricing_rule2 = PricingRule()
        pricing_rule2.property = pro
        pricing_rule2.specific_day = datetime.strptime("11-1-2022", '%m-%d-%Y').date()
        pricing_rule2.fixed_price = 20
        pricing_rule2.save()

        pricing_rule2 = PricingRule()
        pricing_rule2.property = pro
        pricing_rule2.specific_day = datetime.strptime("11-2-2022", '%m-%d-%Y').date()
        pricing_rule2.min_stay_length = 110
        pricing_rule2.fixed_price = 300
        pricing_rule2.save()

        utility = UtilityCalculateBooking()

        date_start = "11-1-2022"
        date_end = "11-10-2022"
        final_value = utility.calcutate_final_price_booking(pro.id, date_start, date_end)
        pro.delete()
        pricing_rule.delete()
        pricing_rule2.delete()

        self.assertEqual(101, final_value)

    def test_case_6(self):
        pro = Property()
        pro.name = "test"
        pro.base_price = 10
        pro.save()
        pricing_rule = PricingRule()
        pricing_rule.property = pro
        pricing_rule.price_modifier = -10
        pricing_rule.min_stay_length = 10
        pricing_rule.save()

        pricing_rule2 = PricingRule()
        pricing_rule2.property = pro
        pricing_rule2.price_modifier = -20
        pricing_rule2.min_stay_length = 10
        pricing_rule2.save()




        utility = UtilityCalculateBooking()

        date_start = "11-1-2022"
        date_end = "11-10-2022"
        final_value = utility.calcutate_final_price_booking(pro.id, date_start, date_end)
        pro.delete()
        pricing_rule.delete()
        pricing_rule2.delete()

        self.assertEqual(90, final_value)

