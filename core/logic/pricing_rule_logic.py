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


    def validate_data(self,data:dict) -> None:
        """
        the data passed in the form of a dic is validated

        :param data: data to send pricing_rule_id, property_id,
        price_modifier , min_stay_length , fixed_price , specific_day

        :returns: None
        :raises ValueError: is generated when formatting not correct
        """

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

    def create_pricing_rule(self) -> PricingRule:
        """
        the principle rule is created with the validation values


        :returns: an object of type princingRule

        """
        self._pricing_rule = PricingRule()
        self._pricing_rule.property_id = self._property.id
        self._pricing_rule.price_modifier = self._price_modifier
        self._pricing_rule.min_stay_length = self._min_stay_length
        self._pricing_rule.fixed_price = self._fixed_price
        self._pricing_rule.specific_day = self._specific_day
        self._pricing_rule.save()
        return self._pricing_rule

    def update_pricing_rule(self) -> PricingRule:
        """
              update pricing rule

              :returns: an object of type princingRule
              """

        self._pricing_rule.price_modifier = self._price_modifier
        self._pricing_rule.min_stay_length = self._min_stay_length
        self._pricing_rule.fixed_price = self._fixed_price
        self._pricing_rule.specific_day = self._specific_day
        self._pricing_rule.save()
        return  self._pricing_rule


    def get_max_stay_length_pricing_rule_property(self, property_id :int , stay_length :int ) -> int:
        """
              obtain the largest stay length of a property in a given interval

              :param property_id: property id
              :param stay_length: number of booking days
              :returns: returns the greatest of the minimum time of stay of a rule

              """

        self._max_stay_length = PricingRule.objects.filter(property_id=property_id, min_stay_length__lte=stay_length)\
            .aggregate(Max('min_stay_length'))["min_stay_length__max"]
        return self._max_stay_length

    def get_max_value_pricing_rule_property(self,max_stay_length : int , property_id :int , stay_length :int ) -> int:
        """
              returns the largest princingrule modifier

              :param max_stay_length: max stay length
              :param property_id: property id
              :param stay_length: number of booking days
              :returns: this is a description of what is returned
              :raises keyError: raises an exception
              """

        self._max_value = PricingRule.objects.filter(Q(min_stay_length= max_stay_length,
                                                 property_id=property_id,
                                                 min_stay_length__lte=stay_length)
                                               ).aggregate(Max('price_modifier'))["price_modifier__max"]
        return self._max_value

    def filter_get_max_pricing_rule_obj(self, price_modifier : int, property_id : int, stay_length : int) -> PricingRule:
        """
               returns the max pricing rule that satisfies the interval

               :param price_modifier: max price modifier
               :param property_id: property id
               :param stay_length: number of booking days
               :returns: obj PricingRule
               """
        self._max_pricing_rule_obj = PricingRule.objects.filter(Q(price_modifier=price_modifier,
                                                        property_id=property_id,
                                                        min_stay_length__lte=stay_length)) \
            .order_by("id").first()
        if self._max_pricing_rule_obj is None:
            self._max_pricing_rule_obj = PricingRule()
        return self._max_pricing_rule_obj

    def get__max_pricing_rule_obj(self) -> PricingRule:
        return self._max_pricing_rule_obj

    def get_specifict_days_with_max_fixed_price_rule(self,property_id : int, stay_length : int,
                                                     date_start : datetime, date_end : datetime) -> list:
        """
                  get all the dates where there is a price modification in the given indexed

                  :param property_id: property id
                  :param stay_length: number of booking days
                  :param date_start: date start of the interval to search
                  :param date_start: date start of the interval to search


                  :returns: ("specific_day":datetime , "fixed_price":int)
                  """
        query_date = Q()
        query_date &= Q(specific_day__range=(date_start,date_end))
        pricing_rules_none = PricingRule.objects.filter(Q(property_id=property_id))

        pricing_rules_spe_day = pricing_rules_none.filter(Q(specific_day__isnull=False) & query_date)

        exclude = []
        for pricing_rule in pricing_rules_spe_day:
            if pricing_rule.min_stay_length is not None:
                if pricing_rule.min_stay_length > stay_length:
                    exclude.append(pricing_rule.id)

        total = pricing_rules_spe_day.exclude(id__in=exclude)


        list_specif_day_fix_pric= total.values('specific_day').annotate(max_id=Max('fixed_price'))

        return list_specif_day_fix_pric

