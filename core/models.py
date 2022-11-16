from django.db import models


class Property(models.Model):
    """
        Model that represents a property.
        A property could be a house, a flat, a hotel room, etc.
    """
    name = models.CharField(max_length=255, blank=True, null=True)
    """name: Name of the property"""
    base_price = models.FloatField(null=True, blank=True)
    """base_price: base price of the property per day"""
    type = models.CharField(max_length=255, blank=True, null=True)
    """type: type of property house,flat, hoterl room, ect"""

    def get_json_data(self):
        out_json = {
                "property_id":self.id,
                "name": self.name,
                "base_price":self.base_price,
                "type":self.type
                }
        return out_json

class PricingRule(models.Model):
    """
        Model that represents a pricing rule that will be applied to a property when booking.
        A rule can have a fixed price, or a percent modifier.
        Only one rule can apply per day.
        We can have multiple rules for the same day, but only the most relevant rule applies.
    """
    property = models.ForeignKey('core.Property', blank=False, null=False, on_delete=models.CASCADE)
    """property: This rule is applied to a particular property"""
    price_modifier = models.FloatField(null=True, blank=True)
    """price_modifier: Represents a percentage that can be positive (increment) or negative (discount)"""
    min_stay_length = models.IntegerField(null=True, blank=True)
    """min_stay_length: This rule applies only if the stay_length of the booking is >= min_stay_length """
    fixed_price = models.FloatField(null=True, blank=True)
    """fixed_price: A rule can have a fixed price for the given day"""
    specific_day = models.DateField(null=True, blank=True)
    """specific_day: A rule can apply to a specific date. Ex: Christmas"""

    def get_json_data(self):
        out_json = {
                "pricing_rule_id":self.id,
                "property_id"      : self.property_id,
                "price_modifier": self.price_modifier,
                "min_stay_length"      : self.min_stay_length,
                "fixed_price":self.fixed_price,
                "specific_day": self.specific_day
                }
        return out_json

class Booking(models.Model):
    """
        Model that represent a booking.
        A booking is done when a customer books a property for a given range of days.
        The booking model is also in charge of calculating the final price the customer will pay.
    """
    property = models.ForeignKey('core.Property', blank=False, null=False, on_delete=models.CASCADE)
    """property: The property this booking is for"""
    date_start = models.DateField(blank=False, null=False)
    """date_start: First day of the booking"""
    date_end = models.DateField(blank=False, null=False)
    """date_end: Last date of the booking"""
    final_price = models.FloatField(null=True, blank=True)
    """final_price: Calculated final price"""
    pricing_rules_used = models.CharField(max_length=900, blank=True, null=True)
    """pricing_rules_used: princing rule used """
    specific_day_rules_used = models.CharField(max_length=900, blank=True, null=True)
    """specific_day_rules_used: specific days fixed price used """

    def get_json_data(self):
        data_out = {
                "Property base_price ": self.property.base_price,
                "Booking"             : {
                        "date_start" : self.date_start,
                        "date_end"   : self.date_end,
                        "stay length": (self.date_start - self.date_end).days + 1
                        },
                "Pricing Rules"       : {
                        "Pricing Rules": self.pricing_rules_used,
                        "specific_day" : self.specific_day_rules_used
                        },
                "Final Price"         : self.final_price,
                "booking_id "          :self.id
                }
        return data_out