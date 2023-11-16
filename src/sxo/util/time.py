import numpy as np
import datetime as dt
from enum import Enum

class TimeUtilsError(Exception):
    ...

class TimeUnits(Enum):
    NANO = 'ns'
    MICRO = 'us'
    MILLI = 'ms'
    SECOND = 's'
    MINUTE = 'm'
    HOUR = 'h'
    DAY = 'D'
    MONTH = 'M'
    YEAR = 'Y'

    def one_down(self,):
        '''return time units one smaller (e.g. if seconds, return mintues)'''
        all = list(TimeUnits)
        idx = all.index(self)
        if idx > 0:
            return all[idx - 1]
        else:
            return self

    def one_up(self,):
        all = list(TimeUnits)
        idx = all.index(self)
        if idx < len(all) - 1:
            return all[idx + 1]
        else:
            return self

    def np_dt_type(self,):
        '''generate a nunpy datetime64 type string for enum value'''
        return f'datetime64[{self.value}]'

    def np_td_type(self,):
        '''generate a nunpy timedelta64 type string for enum value'''
        return f'timedelta64[{self.value}]'

class TimeUtils:

    @staticmethod
    def str_2_time(time_str:str) :
        raise Exception(f"TODO:>> implement this util, it is useful")

    @staticmethod
    def round(
            time: np.datetime64 | dt.datetime | str,
            granularity:str | TimeUnits,
            up:bool = False,
        ) ->  np.datetime64 | dt.datetime:

        # is string, see if it can be parsed and process as datetime64
        if isinstance(time, str):
            return TimeUtils.round_time(np.datetime64(time), granularity)

        tu = TimeUnits(granularity)

        if isinstance(time, np.datetime64):
            rounded = time.astype(tu.np_dt_type())
            if up and (time - rounded > np.timedelta64(0, 'ns')):
                rounded += np.timedelta64(1, tu.value)
            return rounded
        else:
            raise TimeUtilsError(f'only supporting numpy datetime64 times')


class GranularTime:
    '''
        time with given granularity and some convenience functions
        time with minutes granularity does not have any non-aero seconds etc
    '''
    def __init__(self, t:np.datetime64 = None, units:str | TimeUnits = None):
        if not t:
            t = np.datetime64('now')

        if units:
            tu = TimeUnits(units)
        else:
            tu = TimeUnits.NANO

        rounded = TimeUtils.round(t, tu)
        residual = t - rounded

        self._t = rounded
        self._tu = tu
        self._residual = residual

    def add(self, dt:int | np.timedelta64):
        if isinstance(dt, int):
            dt = np.timedelta64(dt, self._tu.value)
        elif isinstance(dt, np.timedelta64):
            dt = dt.astype(self._tu.np_td_type())

        target_time = self._t + dt
        wrapped = GranularTime(target_time, self._tu)
        wrapped._residual = self._residual
        return wrapped

    def get(self,) -> np.timedelta64:
        return self._t

    def units(self,) -> np.timedelta64:
        return self._tu

    def round(self, boundary_fraction:float): # -> GranularTime:
        '''
        round the granular time up or down depending on its residual.
        if the residual is more than the fraction of the time unit
        round up, else do nothing
        '''

        very_granular_time_units = self._tu.one_down().one_down().one_down()
        very_granular_unit_increment = np.int64(1).astype(self._tu.np_td_type()).astype(very_granular_time_units.np_td_type())

        if self._residual > very_granular_unit_increment * boundary_fraction:
            return self.add(1)
        else:
            return self

    def __str__(self,) -> str:
        return str(self._t)

#     assert np.datetime64('2000-01-31T12:12') == TimeUtils.round_time(np.datetime64('2000-01-31T12:12'), 'm' )
#     assert np.datetime64('2000-01-31T12:12') == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:00'), 'm' )
#     assert np.datetime64('2000-01-31T12:12') == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:00.000'), 'm' )

#     assert np.datetime64('2000-01-31T12:12')        == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:12.000'), 'm' )
#     assert np.datetime64('2000-01-31T12:12:00')     == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:12.000'), 'm' )
#     assert np.datetime64('2000-01-31T12:12:00.000') == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:12.000'), 'm' )

#     assert np.datetime64('2000-01-31T12:13')        == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:12.000'), 'm', round_up=True)
#     assert np.datetime64('2000-01-31T12:13:00')     == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:12.000'), 'm', round_up=True)
#     assert np.datetime64('2000-01-31T12:13:00.000') == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:12.000'), 'm', round_up=True)

#     assert np.datetime64('2000-01-31T12:13') == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:00.001'), 'm' , round_up=True)
#     assert np.datetime64('2000-01-31T12:12:01') == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:00.001'), 's' , round_up=True)
#     assert np.datetime64('2000-01-31T12:12:00.001') == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:00.001'), 'ms' , round_up=True)
#     assert np.datetime64('2000-01-31T12:12:00.001') == TimeUtils.round_time(np.datetime64('2000-01-31T12:12:00.000001'), 'ms' , round_up=True)

if __name__ == "__main__":
    t = TimeUtils.round(np.datetime64('2000-01-31T12:12:00.001'), 'm' , up=True)
    print(str(t))


