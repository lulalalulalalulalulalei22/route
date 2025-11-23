"""
距离矩阵计算模块
"""
import math
from typing import List, Dict
from .models import Location


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    使用Haversine公式计算两点间的大圆距离（公里）
    
    Args:
        lat1, lon1: 第一个地点的纬度和经度
        lat2, lon2: 第二个地点的纬度和经度
    
    Returns:
        两点间的距离（公里）
    """
    # 地球半径（公里）
    R = 6371.0
    
    # 转换为弧度
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine公式
    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance


def manhattan_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    计算曼哈顿距离（适用于城市网格道路）
    
    Args:
        lat1, lon1: 第一个地点的纬度和经度
        lat2, lon2: 第二个地点的纬度和经度
    
    Returns:
        两点间的曼哈顿距离（公里）
    """
    # 粗略估算：1度纬度约111公里，1度经度约111*cos(纬度)公里
    avg_lat = (lat1 + lat2) / 2
    lat_distance = abs(lat1 - lat2) * 111.0
    lon_distance = abs(lon1 - lon2) * 111.0 * math.cos(math.radians(avg_lat))
    
    return lat_distance + lon_distance


class DistanceMatrix:
    """距离矩阵计算器"""
    
    def __init__(self, locations: List[Location], distance_type: str = 'haversine'):
        """
        初始化距离矩阵
        
        Args:
            locations: 地点列表
            distance_type: 距离计算类型 ('haversine' 或 'manhattan')
        """
        self.locations = locations
        self.distance_type = distance_type
        self.matrix: Dict[Tuple[int, int], float] = {}
        self._compute_matrix()
    
    def _compute_matrix(self):
        """计算所有地点间的距离矩阵"""
        n = len(self.locations)
        for i in range(n):
            for j in range(n):
                if i == j:
                    self.matrix[(i, j)] = 0.0
                else:
                    loc1 = self.locations[i]
                    loc2 = self.locations[j]
                    
                    if self.distance_type == 'haversine':
                        dist = haversine_distance(
                            loc1.latitude, loc1.longitude,
                            loc2.latitude, loc2.longitude
                        )
                    else:  # manhattan
                        dist = manhattan_distance(
                            loc1.latitude, loc1.longitude,
                            loc2.latitude, loc2.longitude
                        )
                    
                    self.matrix[(i, j)] = dist
    
    def get_distance(self, from_idx: int, to_idx: int) -> float:
        """
        获取两个地点间的距离
        
        Args:
            from_idx: 起始地点索引
            to_idx: 目标地点索引
        
        Returns:
            距离（公里）
        """
        return self.matrix.get((from_idx, to_idx), float('inf'))
    
    def get_travel_time(self, from_idx: int, to_idx: int, avg_speed: float = 30.0) -> float:
        """
        计算两点间的旅行时间
        
        Args:
            from_idx: 起始地点索引
            to_idx: 目标地点索引
            avg_speed: 平均速度（公里/小时）
        
        Returns:
            旅行时间（分钟）
        """
        distance = self.get_distance(from_idx, to_idx)
        return (distance / avg_speed) * 60  # 转换为分钟
    
    def __str__(self):
        """字符串表示"""
        n = len(self.locations)
        lines = ["距离矩阵（公里）:"]
        lines.append("    " + " ".join(f"{i:6d}" for i in range(n)))
        for i in range(n):
            line = f"{i:3d} " + " ".join(f"{self.get_distance(i, j):6.2f}" for j in range(n))
            lines.append(line)
        return "\n".join(lines)

