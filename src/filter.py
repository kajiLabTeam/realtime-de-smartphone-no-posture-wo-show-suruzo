from typing import List

from ahrs.filters import Madgwick

from src.type import Quaternion, SensorData


class FilterBase:
    """
    フィルターの基底クラス
    """

    last_quaternion: Quaternion = [1.0, 0.0, 0.0, 0.0]

    def __init__(self, initQuaternion: Quaternion = None) -> None:
        if initQuaternion is not None:
            self.last_quaternion = initQuaternion

    def init(self, initQuaternion: Quaternion) -> None:
        """
        フィルターの初期化処理
        """
        self.last_quaternion = initQuaternion

    def update(self, sensorData: SensorData = [1.0, 0.0, 0.0, 0.0]) -> List[Quaternion]:
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
        q = self.last_quaternion
        print(q)
        new_quaternion = [[q[0] + i, q[1], q[2], q[3]] for i in range(len(sensorData))]
        self.last_quaternion = new_quaternion[-1]

        return new_quaternion


class MadgwickFilter(FilterBase):
    """
    読み方わからんフィルター
    """

    def update(self, sensorData: SensorData) -> List[Quaternion]:
        sampling_rate = 100  # デフォ値
        madgwick = Madgwick(frequency=sampling_rate, gain_imu=0.33)
        q = self.last_quaternion
        print(q)
        # 各センサーデータに対してクォータニオンを更新し、リストに追加
        quaternions = []
        for data in sensorData:
            q = madgwick.updateIMU(
                q=q,
                gyr=[data.gyroscope.x, data.gyroscope.y, data.gyroscope.z],
                acc=[data.acceleration.x, data.acceleration.y, data.acceleration.z],
            )
            # new_quaternion = [q[0], q[1], q[2], q[3]]
            quaternions.append([q[0], q[1], q[2], q[3]])

        self.last_quaternion = quaternions[-1]

        return quaternions
