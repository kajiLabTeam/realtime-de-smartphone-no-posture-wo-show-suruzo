from typing import List
from src.type import FrameData, Quaternion, SensorData
import math


class FilterBase:
    """
    フィルターの基底クラス
    """

    current_quaternion: Quaternion = [1.0, 0.0, 0.0, 0.0]

    def __init__(self, initQuaternion: Quaternion = None) -> None:
        if initQuaternion is not None:
            self.current_quaternion = initQuaternion

    def update(self, sensorData: SensorData) -> List[Quaternion]:
        """
        フィルターの更新処理
        """
        raise NotImplementedError("サブクラスで実装してください。")


class SampleFilter(FilterBase):
    """
    サンプルのフィルター
    """

    def update(self, sensorData: SensorData) -> List[Quaternion]:
        """
        フィルターのサンプル. 3度ずつ回転する動作を返す
        """
        return [[0, math.pi / 60 * i, 0] for i in range(len(sensorData))]
