"""
时间窗口约束处理模块
"""
from typing import List, Tuple
from datetime import time, datetime, timedelta
from .models import Location, RouteSolution
from .distance_matrix import DistanceMatrix


def time_to_minutes(t: time) -> int:
    """将time对象转换为从午夜开始的分钟数"""
    return t.hour * 60 + t.minute


def minutes_to_time(minutes: int) -> time:
    """将分钟数转换为time对象"""
    hours = minutes // 60
    mins = minutes % 60
    return time(hour=hours % 24, minute=mins)


class ConstraintChecker:
    """约束检查器"""
    
    def __init__(self, locations: List[Location], distance_matrix: DistanceMatrix, 
                 avg_speed: float = 30.0, start_time: time = time(9, 0)):
        """
        初始化约束检查器
        
        Args:
            locations: 地点列表
            distance_matrix: 距离矩阵
            avg_speed: 平均速度（公里/小时）
            start_time: 出发时间
        """
        self.locations = locations
        self.distance_matrix = distance_matrix
        self.avg_speed = avg_speed
        self.start_time_minutes = time_to_minutes(start_time)
    
    def check_time_window(self, location_idx: int, arrival_time: float) -> Tuple[bool, float]:
        """
        检查时间窗口约束
        
        Args:
            location_idx: 地点索引
            arrival_time: 到达时间（分钟，从出发时间开始计算）
        
        Returns:
            (是否满足约束, 实际到达时间)
        """
        location = self.locations[location_idx]
        
        # 如果没有时间窗口约束，直接返回
        if location.open_time is None or location.close_time is None:
            return True, arrival_time
        
        # 计算实际时间（从午夜开始的分钟数）
        actual_time_minutes = self.start_time_minutes + arrival_time
        
        # 处理跨天情况
        open_minutes = time_to_minutes(location.open_time)
        close_minutes = time_to_minutes(location.close_time)
        
        # 如果关闭时间小于开放时间，说明跨天
        if close_minutes < open_minutes:
            close_minutes += 24 * 60
        
        # 标准化实际时间到同一天
        actual_time_normalized = actual_time_minutes % (24 * 60)
        
        # 检查是否在时间窗口内
        if open_minutes <= close_minutes:
            # 正常情况：开放时间 < 关闭时间
            if open_minutes <= actual_time_normalized <= close_minutes:
                return True, arrival_time
            else:
                # 需要等待到开放时间
                if actual_time_normalized < open_minutes:
                    wait_time = open_minutes - actual_time_normalized
                else:
                    # 需要等到第二天
                    wait_time = (24 * 60 - actual_time_normalized) + open_minutes
                return False, arrival_time + wait_time
        else:
            # 跨天情况
            if actual_time_normalized >= open_minutes or actual_time_normalized <= close_minutes:
                return True, arrival_time
            else:
                wait_time = open_minutes - actual_time_normalized
                return False, arrival_time + wait_time
    
    def evaluate_route(self, route: List[int]) -> RouteSolution:
        """
        评估路径，计算总距离、总时间和约束违反情况
        
        Args:
            route: 地点索引序列
        
        Returns:
            RouteSolution对象
        """
        if not route:
            return RouteSolution(
                route=[],
                total_distance=0.0,
                total_time=0.0,
                fitness=float('inf'),
                violations=0,
                arrival_times=[]
            )
        
        total_distance = 0.0
        current_time = 0.0  # 从出发时间开始的分钟数
        arrival_times = []
        violations = 0
        
        # 从起点开始
        for i in range(len(route)):
            location_idx = route[i]
            location = self.locations[location_idx]
            
            # 记录到达时间
            arrival_times.append(current_time)
            
            # 检查时间窗口约束
            is_valid, actual_arrival = self.check_time_window(location_idx, current_time)
            if not is_valid:
                violations += 1
            current_time = actual_arrival
            
            # 停留时间
            current_time += location.stay_duration
            
            # 前往下一个地点
            if i < len(route) - 1:
                next_idx = route[i + 1]
                distance = self.distance_matrix.get_distance(location_idx, next_idx)
                travel_time = self.distance_matrix.get_travel_time(
                    location_idx, next_idx, self.avg_speed
                )
                total_distance += distance
                current_time += travel_time
        
        total_time = current_time
        
        # 计算适应度：总距离 + 惩罚项（违反约束）
        penalty = violations * 1000.0  # 每个违反约束的惩罚
        fitness = total_distance + penalty
        
        return RouteSolution(
            route=route,
            total_distance=total_distance,
            total_time=total_time,
            fitness=fitness,
            violations=violations,
            arrival_times=arrival_times
        )

