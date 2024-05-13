from functools import cached_property


class TimeData():

    day_to_name = {
      0: 'Monday',
      1: 'Tuesday',
      2: 'Wednesday',
      3: 'Thursday',
      4: 'Friday',
      5: 'Saturday',
      6: 'Sunday'
    }

    def __init__(self, timestamp):
        self.timestamp = timestamp
        self._weeks = None
        self._day_of_week = None
        self._hours = None
        self._minutes = None

    def __add__(self, seconds):
        return TimeData(self.timestamp + seconds)

    def set_data(self):
        nb_seconds = self.timestamp
        nb_minutes = nb_seconds // 60
        nb_hours = nb_minutes // 60
        nb_days = nb_hours // 24
        self._week = nb_days // 7
        remaining_days = nb_days - self._week * 7
        self._hours = nb_hours - nb_days * 24
        self._minutes = nb_minutes - nb_hours * 60
        self._day_of_week = remaining_days % 7

    @cached_property
    def week(self):
        if self._week is None:
            self.set_data()
        return self._week

    @cached_property
    def day_of_week(self):
        if self._day_of_week is None:
            self.set_data()
        return self._day_of_week

    @cached_property
    def hours(self):
        if self._hours is None:
            self.set_data()
        return self._hours

    @cached_property
    def minutes(self):
        if self._minutes is None:
            self.set_data()
        return self._minutes

    @property
    def week_text(self):
        return f'Week {self.week + 1}'

    @property
    def day_of_week_text(self):
        return f'{self.day_to_name[self.day_of_week]}'

    @property
    def hours_text(self):
        return f'{self.hours:02d}'

    @property
    def minutes_text(self):
        return f'{self.minutes:02d}'
