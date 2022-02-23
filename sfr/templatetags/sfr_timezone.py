from django import template
from sfr.models import *
import pytz

register = template.Library()


@register.simple_tag()
def get_moscow_time(utc_dt):
    local_tz = pytz.timezone('Europe/Moscow')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    utc_to_local = local_tz.normalize(local_dt)
    return utc_to_local.strftime('%H:%M:%S')


@register.simple_tag()
def get_moscow_date(utc_dt):
    local_tz = pytz.timezone('Europe/Moscow')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    utc_to_local = local_tz.normalize(local_dt)
    return utc_to_local.strftime('%d-%m-%Y')
