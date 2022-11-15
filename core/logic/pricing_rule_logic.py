from datetime import datetime

from django.db.models import Max
from django.db.models import Q

from core.models import PricingRule
from core.models import Property
from core.utility.utility_code import ValidationDate


class PricingRuleLogic():

    def __init__(self):
        self._pricing_rule : PricingRule = None
        self._property : Property = None
        self._price_modifier : float = None
        self._min_stay_length : int = None
        self._fixed_price : float = None
        self._specific_day : datetime = None

    def validate_data(self,data:dict):

        utility_date = ValidationDate()

        if "pricing_rule_id" in data:
            self._pricing_rule = PricingRule.objects.get(id=data["pricing_rule_id"])

        if "property_id" in data:
            self._property = Property.objects.get(id = data["property_id"])

        if "price_modifier" in data:
            if data["price_modifier"] is not None:
                self._price_modifier = float(data["price_modifier"])

        if "min_stay_length" in data:
            if data["min_stay_length"] is not None:
                self._min_stay_length = int(data["min_stay_length"])

        if "fixed_price" in data:
            if data["fixed_price"] is not None:
                self._fixed_price = float(data["fixed_price"])

        if "specific_day" in data:
            if data["specific_day"] is not None:
                self._specific_day = utility_date.parse_formate_date(data["specific_day"])

    def create_pricing_rule(self):
        self._pricing_rule = PricingRule()
        self._pricing_rule.property_id = self._property.id
        self._pricing_rule.price_modifier = self._price_modifier
        self._pricing_rule.min_stay_length = self._min_stay_length
        self._pricing_rule.fixed_price = self._fixed_price
        self._pricing_rule.specific_day = self._specific_day
        self._pricing_rule.save()
        return self._pricing_rule

    def update_pricing_rule(self):
        self._pricing_rule.price_modifier = self._price_modifier
        self._pricing_rule.min_stay_length = self._min_stay_length
        self._pricing_rule.fixed_price = self._fixed_price
        self._pricing_rule.specific_day = self._specific_day
        self._pricing_rule.save()
        return  self._pricing_rule

    def get_max_stay_length_pricing_rule_property(self, property_id :int , stay_length :int ):
        self._max_stay_length = PricingRule.objects.filter(property_id=property_id, min_stay_length__lte=stay_length)\
            .aggregate(Max('min_stay_length'))["min_stay_length__max"]
        return self._max_stay_length

    def get_max_value_pricing_rule_property(self,max_stay_length : int , property_id :int , stay_length :int ):
        self._max_value = PricingRule.objects.filter(Q(min_stay_length= max_stay_length,
                                                 property_id=property_id,
                                                 min_stay_length__lte=stay_length)
                                               ).aggregate(Max('price_modifier'))["price_modifier__max"]
        return self._max_value

    def get_max_pricing_rule_obj(self,price_modifier,property_id,stay_length):
        self._max_pricing_rule_obj = PricingRule.objects.filter(Q(price_modifier=price_modifier,
                                                        property_id=property_id,
                                                        min_stay_length__lte=stay_length)) \
            .order_by("id").first()
        return self._max_pricing_rule_obj

    def get_specifict_days_with_max_fixed_price_rule(self,property_id : int, stay_length : int,
                                                     date_start : datetime, date_end : datetime):
        query_date = Q()
        query_date &= Q(specific_day__range=(date_start,date_end))
        pricing_rules = PricingRule.objects.filter(Q(property_id=property_id, min_stay_length__lte=stay_length))

        pricing_rules_spe_day = pricing_rules.filter(Q(specific_day__isnull=False) & query_date)
        list_specif_day_fix_pric= pricing_rules_spe_day.values('specific_day').annotate(max_id=Max('fixed_price'))
        return list_specif_day_fix_pric

