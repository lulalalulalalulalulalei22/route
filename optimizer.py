"""
路径优化器主类
"""
from typing import List, Optional
from .models import Location, RouteSolution
from .distance_matrix import DistanceMatrix
from .constraints import ConstraintChecker
from .genetic_algorithm import GeneticAlgorithm
from .simulated_annealing import SimulatedAnnealing
from datetime import time


class RouteOptimizer:
    """路径优化器主类"""
    
    def __init__(self,
                 locations: List[Location],
                 avg_speed: float = 30.0,
                 start_time: time = time(9, 0),
                 distance_type: str = 'haversine'):
        """
        初始化路径优化器
        
        Args:
            locations: 地点列表
            avg_speed: 平均速度（公里/小时）
            start_time: 出发时间
            distance_type: 距离计算类型 ('haversine' 或 'manhattan')
        """
        self.locations = locations
        self.avg_speed = avg_speed
        self.start_time = start_time
        self.distance_type = distance_type
        
        # 初始化距离矩阵和约束检查器
        self.distance_matrix = DistanceMatrix(locations, distance_type)
        self.constraint_checker = ConstraintChecker(
            locations, self.distance_matrix, avg_speed, start_time
        )
    
    def optimize_genetic(self,
                        population_size: int = 100,
                        generations: int = 200,
                        mutation_rate: float = 0.1,
                        crossover_rate: float = 0.8,
                        elite_size: int = 10) -> RouteSolution:
        """
        使用遗传算法优化路径
        
        Args:
            population_size: 种群大小
            generations: 迭代代数
            mutation_rate: 变异率
            crossover_rate: 交叉率
            elite_size: 精英个体数量
        
        Returns:
            最优路径解决方案
        """
        ga = GeneticAlgorithm(
            self.locations,
            self.constraint_checker,
            population_size,
            generations,
            mutation_rate,
            crossover_rate,
            elite_size
        )
        return ga.optimize()
    
    def optimize_simulated_annealing(self,
                                    initial_temperature: float = 1000.0,
                                    cooling_rate: float = 0.995,
                                    min_temperature: float = 0.1,
                                    iterations_per_temp: int = 100) -> RouteSolution:
        """
        使用模拟退火算法优化路径
        
        Args:
            initial_temperature: 初始温度
            cooling_rate: 冷却速率
            min_temperature: 最低温度
            iterations_per_temp: 每个温度下的迭代次数
        
        Returns:
            最优路径解决方案
        """
        sa = SimulatedAnnealing(
            self.locations,
            self.constraint_checker,
            initial_temperature,
            cooling_rate,
            min_temperature,
            iterations_per_temp
        )
        return sa.optimize()
    
    def optimize(self, algorithm: str = 'genetic', **kwargs) -> RouteSolution:
        """
        优化路径（统一接口）
        
        Args:
            algorithm: 算法类型 ('genetic' 或 'simulated_annealing')
            **kwargs: 算法特定参数
        
        Returns:
            最优路径解决方案
        """
        if algorithm == 'genetic':
            return self.optimize_genetic(**kwargs)
        elif algorithm == 'simulated_annealing':
            return self.optimize_simulated_annealing(**kwargs)
        else:
            raise ValueError(f"未知算法: {algorithm}")
    
    def evaluate_route(self, route: List[int]) -> RouteSolution:
        """评估给定路径"""
        return self.constraint_checker.evaluate_route(route)
    
    def get_distance_matrix(self) -> DistanceMatrix:
        """获取距离矩阵"""
        return self.distance_matrix

