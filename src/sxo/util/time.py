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
    def round_time(
            time: np.datetime64 | dt.datetime | str,
            granularity:str,
            round_up:bool = False,
        ) ->  np.datetime64 | dt.datetime:

        # is string, see if it can be parsed and process as datetime64
        if isinstance(time, str):
            return TimeUtils.round_time(np.datetime64(time), granularity)

        tu = TimeUnits(granularity)

        if isinstance(time, np.datetime64):
            rounded = time.astype(tu.np_dt_type())
            if round_up and (time - rounded > np.timedelta64(0, 'ns')):
                rounded += np.timedelta64(1, tu.value)
            return rounded
        else:
            raise TimeUtilsError(f'only supporting numpy datetime64 times')


# if __name__ == "__main__":
#     # no rounding needed
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
