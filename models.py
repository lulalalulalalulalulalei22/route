"""
地点和时间窗口模型定义
"""
from dataclasses import dataclass
from typing import Optional, Tuple
from datetime import time


@dataclass
class Location:
    """地点信息"""
    id: int
    name: str
    latitude: float  # 纬度
    longitude: float  # 经度
    open_time: Optional[time] = None  # 开放时间
    close_time: Optional[time] = None  # 关闭时间
    stay_duration: int = 0  # 停留时间（分钟）
    priority: float = 1.0  # 优先级（1.0为正常，越高越重要）
    
    def __post_init__(self):
        """验证时间窗口"""
        if self.open_time and self.close_time:
            if self.open_time >= self.close_time:
                raise ValueError(f"地点 {self.name} 的开放时间必须早于关闭时间")


@dataclass
class RouteSolution:
    """路径解决方案"""
    route: list[int]  # 地点ID序列
    total_distance: float  # 总距离（公里）
    total_time: float  # 总时间（分钟）
    fitness: float  # 适应度值（越小越好）
    violations: int  # 违反约束的次数
    arrival_times: list[float]  # 每个地点的到达时间（分钟，从0开始）
    
    def __str__(self):
        return (f"路径: {' -> '.join(map(str, self.route))}\n"
                f"总距离: {self.total_distance:.2f} 公里\n"
                f"总时间: {self.total_time:.2f} 分钟\n"
                f"适应度: {self.fitness:.2f}\n"
                f"违反约束: {self.violations} 次")

