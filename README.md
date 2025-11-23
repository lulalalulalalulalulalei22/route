# 路径优化系统

一个基于时间窗口约束的路径优化系统，使用遗传算法和模拟退火算法寻找最优路径。

## 功能特性

1. **距离矩阵计算**
   - 支持Haversine公式（大圆距离）
   - 支持曼哈顿距离（城市网格道路）
   - 自动计算所有地点间的距离

2. **时间窗口约束**
   - 支持地点开放时间/关闭时间
   - 支持停留时间设置
   - 自动处理等待时间

3. **优化算法**
   - 遗传算法（Genetic Algorithm）
   - 模拟退火算法（Simulated Annealing）
   - 可配置算法参数

4. **平衡效率与用户体验**
   - 考虑总距离最小化
   - 考虑时间窗口约束
   - 支持地点优先级设置

## 安装

本项目主要使用Python标准库，无需额外安装依赖。

```bash
# 克隆或下载项目
# 确保Python版本 >= 3.7
python --version
```

## 使用方法

### 基本使用

```python
from datetime import time
from route_optimizer import Location, RouteOptimizer

# 创建地点列表
locations = [
    Location(
        id=0,
        name="地点A",
        latitude=39.9042,
        longitude=116.4074,
        open_time=time(9, 0),
        close_time=time(18, 0),
        stay_duration=60,  # 停留60分钟
        priority=1.0
    ),
    # ... 更多地点
]

# 创建优化器
optimizer = RouteOptimizer(
    locations=locations,
    avg_speed=30.0,  # 平均速度30公里/小时
    start_time=time(9, 0),  # 出发时间
    distance_type='haversine'  # 或 'manhattan'
)

# 使用遗传算法优化
solution = optimizer.optimize_genetic(
    population_size=100,
    generations=200,
    mutation_rate=0.1,
    crossover_rate=0.8
)

# 或使用模拟退火算法
solution = optimizer.optimize_simulated_annealing(
    initial_temperature=1000.0,
    cooling_rate=0.995
)

# 查看结果
print(solution)
```

### 运行示例

```bash
cd C:\Users\myf11\route_optimizer_project
python example.py
```

## 项目结构

```
route_optimizer_project/
├── route_optimizer/
│   ├── __init__.py              # 包初始化
│   ├── models.py                # 数据模型（Location, RouteSolution）
│   ├── distance_matrix.py       # 距离矩阵计算
│   ├── constraints.py          # 时间窗口约束处理
│   ├── genetic_algorithm.py     # 遗传算法实现
│   ├── simulated_annealing.py   # 模拟退火算法实现
│   └── optimizer.py            # 优化器主类
├── example.py                   # 使用示例
├── requirements.txt             # 依赖文件
└── README.md                    # 说明文档
```

## 核心思路

1. **计算所有地点间的距离矩阵**
   - 使用Haversine公式计算地理距离
   - 支持曼哈顿距离用于城市道路
   - 预计算所有地点对的距离，提高效率

2. **考虑时间窗口约束**
   - 检查每个地点的到达时间是否在开放时间内
   - 如果不在，计算等待时间
   - 考虑停留时间对后续行程的影响

3. **使用优化算法寻找最优路径**
   - **遗传算法**：适合大规模问题，通过种群进化寻找最优解
   - **模拟退火**：适合中小规模问题，通过温度控制避免局部最优

4. **平衡效率与用户体验**
   - 适应度函数 = 总距离 + 违反约束惩罚
   - 支持地点优先级（可在未来扩展）
   - 提供详细的路径信息（到达时间、停留时间等）

## 算法参数说明

### 遗传算法参数

- `population_size`: 种群大小（默认100）
- `generations`: 迭代代数（默认200）
- `mutation_rate`: 变异率（默认0.1）
- `crossover_rate`: 交叉率（默认0.8）
- `elite_size`: 精英个体数量（默认10）

### 模拟退火算法参数

- `initial_temperature`: 初始温度（默认1000.0）
- `cooling_rate`: 冷却速率（默认0.995）
- `min_temperature`: 最低温度（默认0.1）
- `iterations_per_temp`: 每个温度下的迭代次数（默认100）

## 扩展建议

1. **可视化功能**
   - 在地图上显示优化后的路径
   - 显示时间轴和地点访问顺序

2. **更多约束**
   - 最大总时间限制
   - 地点之间的依赖关系
   - 多车辆路径规划

3. **性能优化**
   - 使用并行计算加速遗传算法
   - 实现更高效的邻域搜索

4. **算法扩展**
   - 蚁群算法（ACO）
   - 粒子群优化（PSO）
   - 混合算法

## 许可证

MIT License

