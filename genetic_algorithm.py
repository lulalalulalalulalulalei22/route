"""
遗传算法优化器
"""
import random
import copy
from typing import List, Tuple
from .models import Location, RouteSolution
from .constraints import ConstraintChecker


class GeneticAlgorithm:
    """遗传算法路径优化器"""
    
    def __init__(self, 
                 locations: List[Location],
                 constraint_checker: ConstraintChecker,
                 population_size: int = 100,
                 generations: int = 200,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.8,
                 elite_size: int = 10):
        """
        初始化遗传算法
        
        Args:
            locations: 地点列表
            constraint_checker: 约束检查器
            population_size: 种群大小
            generations: 迭代代数
            mutation_rate: 变异率
            crossover_rate: 交叉率
            elite_size: 精英个体数量
        """
        self.locations = locations
        self.constraint_checker = constraint_checker
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        self.num_locations = len(locations)
    
    def create_individual(self) -> List[int]:
        """创建随机个体（路径）"""
        route = list(range(self.num_locations))
        random.shuffle(route)
        return route
    
    def create_population(self) -> List[List[int]]:
        """创建初始种群"""
        return [self.create_individual() for _ in range(self.population_size)]
    
    def fitness(self, route: List[int]) -> float:
        """计算适应度（越小越好）"""
        solution = self.constraint_checker.evaluate_route(route)
        return solution.fitness
    
    def rank_population(self, population: List[List[int]]) -> List[Tuple[float, List[int]]]:
        """对种群进行排序（按适应度）"""
        fitness_results = [(self.fitness(individual), individual) for individual in population]
        return sorted(fitness_results, key=lambda x: x[0])
    
    def selection(self, ranked_population: List[Tuple[float, List[int]]]) -> List[int]:
        """选择操作（轮盘赌选择）"""
        # 使用倒数作为选择概率（适应度越小，概率越大）
        fitnesses = [1.0 / (1.0 + rank[0]) for rank in ranked_population]
        total_fitness = sum(fitnesses)
        probabilities = [f / total_fitness for f in fitnesses]
        
        # 累积概率
        cumulative = []
        cumsum = 0
        for p in probabilities:
            cumsum += p
            cumulative.append(cumsum)
        
        # 轮盘赌选择
        r = random.random()
        for i, cum_prob in enumerate(cumulative):
            if r <= cum_prob:
                return ranked_population[i][1]
        return ranked_population[-1][1]
    
    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """交叉操作（顺序交叉）"""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        # 选择交叉点
        point1 = random.randint(0, len(parent1) - 1)
        point2 = random.randint(0, len(parent1) - 1)
        if point1 > point2:
            point1, point2 = point2, point1
        
        # 创建子代1
        child1 = [-1] * len(parent1)
        child1[point1:point2+1] = parent1[point1:point2+1]
        
        # 从parent2填充剩余位置
        pos = 0
        for gene in parent2:
            if gene not in child1:
                while child1[pos] != -1:
                    pos += 1
                child1[pos] = gene
        
        # 创建子代2
        child2 = [-1] * len(parent2)
        child2[point1:point2+1] = parent2[point1:point2+1]
        
        pos = 0
        for gene in parent1:
            if gene not in child2:
                while child2[pos] != -1:
                    pos += 1
                child2[pos] = gene
        
        return child1, child2
    
    def mutate(self, individual: List[int]) -> List[int]:
        """变异操作（交换两个随机位置）"""
        if random.random() > self.mutation_rate:
            return individual
        
        mutated = individual.copy()
        idx1, idx2 = random.sample(range(len(mutated)), 2)
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
        return mutated
    
    def evolve(self, population: List[List[int]]) -> List[List[int]]:
        """进化一代"""
        # 排序种群
        ranked = self.rank_population(population)
        
        # 保留精英
        elite = [individual for _, individual in ranked[:self.elite_size]]
        
        # 生成新种群
        new_population = elite.copy()
        
        while len(new_population) < self.population_size:
            # 选择父代
            parent1 = self.selection(ranked)
            parent2 = self.selection(ranked)
            
            # 交叉
            child1, child2 = self.crossover(parent1, parent2)
            
            # 变异
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            
            new_population.append(child1)
            if len(new_population) < self.population_size:
                new_population.append(child2)
        
        return new_population
    
    def optimize(self) -> RouteSolution:
        """执行优化"""
        # 创建初始种群
        population = self.create_population()
        
        # 记录最佳解
        best_solution = None
        best_fitness = float('inf')
        
        # 进化
        for generation in range(self.generations):
            population = self.evolve(population)
            
            # 更新最佳解
            ranked = self.rank_population(population)
            current_best_fitness, current_best_individual = ranked[0]
            
            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_solution = self.constraint_checker.evaluate_route(current_best_individual)
            
            # 每10代输出一次进度
            if (generation + 1) % 10 == 0:
                print(f"第 {generation + 1} 代: 最佳适应度 = {best_fitness:.2f}, "
                      f"违反约束 = {best_solution.violations if best_solution else 0}")
        
        return best_solution if best_solution else self.constraint_checker.evaluate_route(population[0])

