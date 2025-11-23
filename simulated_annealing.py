"""
模拟退火算法优化器
"""
import random
import math
from typing import List
from .models import Location, RouteSolution
from .constraints import ConstraintChecker


class SimulatedAnnealing:
    """模拟退火算法路径优化器"""
    
    def __init__(self,
                 locations: List[Location],
                 constraint_checker: ConstraintChecker,
                 initial_temperature: float = 1000.0,
                 cooling_rate: float = 0.995,
                 min_temperature: float = 0.1,
                 iterations_per_temp: int = 100):
        """
        初始化模拟退火算法
        
        Args:
            locations: 地点列表
            constraint_checker: 约束检查器
            initial_temperature: 初始温度
            cooling_rate: 冷却速率
            min_temperature: 最低温度
            iterations_per_temp: 每个温度下的迭代次数
        """
        self.locations = locations
        self.constraint_checker = constraint_checker
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
        self.iterations_per_temp = iterations_per_temp
        self.num_locations = len(locations)
    
    def create_initial_solution(self) -> List[int]:
        """创建初始解"""
        route = list(range(self.num_locations))
        random.shuffle(route)
        return route
    
    def get_neighbor(self, route: List[int]) -> List[int]:
        """生成邻域解（交换两个随机位置）"""
        neighbor = route.copy()
        idx1, idx2 = random.sample(range(len(neighbor)), 2)
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
        return neighbor
    
    def acceptance_probability(self, current_fitness: float, new_fitness: float, temperature: float) -> float:
        """计算接受概率"""
        if new_fitness < current_fitness:
            return 1.0
        return math.exp(-(new_fitness - current_fitness) / temperature)
    
    def optimize(self) -> RouteSolution:
        """执行优化"""
        # 初始化
        current_route = self.create_initial_solution()
        current_solution = self.constraint_checker.evaluate_route(current_route)
        best_route = current_route.copy()
        best_solution = current_solution
        
        temperature = self.initial_temperature
        iteration = 0
        
        while temperature > self.min_temperature:
            for _ in range(self.iterations_per_temp):
                # 生成邻域解
                neighbor_route = self.get_neighbor(current_route)
                neighbor_solution = self.constraint_checker.evaluate_route(neighbor_route)
                
                # 决定是否接受新解
                if self.acceptance_probability(
                    current_solution.fitness,
                    neighbor_solution.fitness,
                    temperature
                ) > random.random():
                    current_route = neighbor_route
                    current_solution = neighbor_solution
                
                # 更新最佳解
                if current_solution.fitness < best_solution.fitness:
                    best_route = current_route.copy()
                    best_solution = current_solution
            
            # 降温
            temperature *= self.cooling_rate
            iteration += 1
            
            # 每10次迭代输出一次进度
            if iteration % 10 == 0:
                print(f"温度: {temperature:.2f}, 最佳适应度: {best_solution.fitness:.2f}, "
                      f"违反约束: {best_solution.violations}")
        
        return best_solution

