from sxo.util.runtime.config import ConfigBase
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.interface.entities.instruments import Instrument


class StrategyConfig(ConfigBase):
    INSTRUMENT = "STRATEGY_INSTRUMENT"
    TRADE_FREQUENCY = "STRATEGY_TRADE_FREQUENCY"
    ALPHA = "STRATEGY_ALPHA"
    BETA = "STRATEGY_BETA"

    def __init__(self,):
        instr_str = self.get_str(StrategyConfig.INSTRUMENT)
        self._inst = InstrumentUtil.parse(instr_str)
        self._freq = self.get_int(StrategyConfig.TRADE_FREQUENCY)
        self._alph = self.get_float(StrategyConfig.ALPHA)
        self._beta = self.get_float(StrategyConfig.BETA)

    def instrument(self,) -> Instrument:
        return self._inst

    def frequency(self,) -> int:
        return self._freq

    def alpha(self,) -> float:
        return self._alph

    def beta(self,) -> float:
        return self._beta
