import datetime

def to_event(eve: str):
    return eve.strip().lower()

def datetime_to_dict(dt: datetime.datetime):
    return {
		'year':dt.year,
		'month':dt.month,
		'day':dt.day,
		'hour':dt.hour,
		'minute':dt.minute,
		'second':dt.second,
		'millisecond':dt.microsecond
	}