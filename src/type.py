from typing import List
from pydantic import BaseModel, ValidationError


class Acceleration(BaseModel):
    """
    加速度センサーのデータ
    """
    x: float
    y: float
    z: float


class Gyroscope(BaseModel):
    """
    ジャイロセンサーのデータ
    """
    x: float
    y: float
    z: float


class FrameData(BaseModel):
    """
    1フレームのセンサーデータ
    """

    timestamp: float
    acceleration: Acceleration
    gyroscope: Gyroscope


# センサーデータの型
SensorData = List[FrameData]

# クォータニオンの型
Quaternion = List[float]


def validate_sensor_data(data: list) -> SensorData | None:
    """
    センサーデータのバリデーションを行う
    """

    try:
        return [FrameData(**item) for item in data]
    except ValidationError as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None
