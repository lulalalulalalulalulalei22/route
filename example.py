"""
路径优化系统使用示例
"""
from datetime import time
from route_optimizer import Location, RouteOptimizer


def main():
    """主函数"""
    # 创建地点列表（示例：北京的一些景点）
    locations = [
        Location(
            id=0,
            name="天安门广场",
            latitude=39.9042,
            longitude=116.4074,
            open_time=time(6, 0),
            close_time=time(22, 0),
            stay_duration=60,  # 停留1小时
            priority=1.0
        ),
        Location(
            id=1,
            name="故宫博物院",
            latitude=39.9163,
            longitude=116.3972,
            open_time=time(8, 30),
            close_time=time(17, 0),
            stay_duration=180,  # 停留3小时
            priority=1.5
        ),
        Location(
            id=2,
            name="天坛公园",
            latitude=39.8826,
            longitude=116.4070,
            open_time=time(6, 0),
            close_time=time(21, 0),
            stay_duration=90,  # 停留1.5小时
            priority=1.0
        ),
        Location(
            id=3,
            name="颐和园",
            latitude=39.9990,
            longitude=116.2750,
            open_time=time(6, 30),
            close_time=time(18, 0),
            stay_duration=120,  # 停留2小时
            priority=1.2
        ),
        Location(
            id=4,
            name="圆明园",
            latitude=40.0080,
            longitude=116.3000,
            open_time=time(7, 0),
            close_time=time(19, 0),
            stay_duration=90,  # 停留1.5小时
            priority=1.0
        ),
        Location(
            id=5,
            name="鸟巢",
            latitude=39.9930,
            longitude=116.3979,
            open_time=time(9, 0),
            close_time=time(18, 0),
            stay_duration=60,  # 停留1小时
            priority=1.0
        ),
    ]
    
    # 创建优化器
    optimizer = RouteOptimizer(
        locations=locations,
        avg_speed=30.0,  # 平均速度30公里/小时
        start_time=time(9, 0),  # 早上9点出发
        distance_type='haversine'  # 使用Haversine公式计算距离
    )
    
    print("=" * 60)
    print("路径优化系统")
    print("=" * 60)
    print(f"\n地点数量: {len(locations)}")
    print(f"出发时间: {time(9, 0)}")
    print(f"平均速度: 30 公里/小时\n")
    
    # 显示距离矩阵
    print(optimizer.get_distance_matrix())
    print("\n" + "=" * 60)
    
    # 使用遗传算法优化
    print("\n使用遗传算法优化路径...")
    print("-" * 60)
    solution_ga = optimizer.optimize_genetic(
        population_size=100,
        generations=100,
        mutation_rate=0.1,
        crossover_rate=0.8,
        elite_size=10
    )
    
    print("\n遗传算法结果:")
    print(solution_ga)
    print_location_details(locations, solution_ga, optimizer)
    
    # 使用模拟退火算法优化
    print("\n" + "=" * 60)
    print("\n使用模拟退火算法优化路径...")
    print("-" * 60)
    solution_sa = optimizer.optimize_simulated_annealing(
        initial_temperature=1000.0,
        cooling_rate=0.995,
        min_temperature=0.1,
        iterations_per_temp=100
    )
    
    print("\n模拟退火算法结果:")
    print(solution_sa)
    print_location_details(locations, solution_sa, optimizer)
    
    # 比较两种算法
    print("\n" + "=" * 60)
    print("算法比较:")
    print("-" * 60)
    print(f"遗传算法: 总距离 {solution_ga.total_distance:.2f} 公里, "
          f"总时间 {solution_ga.total_time:.2f} 分钟, "
          f"违反约束 {solution_ga.violations} 次")
    print(f"模拟退火: 总距离 {solution_sa.total_distance:.2f} 公里, "
          f"总时间 {solution_sa.total_time:.2f} 分钟, "
          f"违反约束 {solution_sa.violations} 次")


def print_location_details(locations, solution, optimizer):
    """打印路径详细信息"""
    from datetime import time, timedelta, datetime
    
    print("\n详细路径信息:")
    print("-" * 60)
    
    start_time = time(9, 0)
    current_time = start_time
    
    for i, loc_idx in enumerate(solution.route):
        location = locations[loc_idx]
        arrival_minutes = solution.arrival_times[i]
        
        # 计算到达时间
        arrival_delta = timedelta(minutes=int(arrival_minutes))
        arrival_time = datetime.combine(datetime.today(), start_time) + arrival_delta
        arrival_time_only = arrival_time.time()
        
        # 计算离开时间
        leave_minutes = arrival_minutes + location.stay_duration
        leave_delta = timedelta(minutes=int(leave_minutes))
        leave_time = datetime.combine(datetime.today(), start_time) + leave_delta
        leave_time_only = leave_time.time()
        
        print(f"\n{i+1}. {location.name}")
        print(f"   到达时间: {arrival_time_only.strftime('%H:%M')}")
        print(f"   停留时间: {location.stay_duration} 分钟")
        print(f"   离开时间: {leave_time_only.strftime('%H:%M')}")
        
        if location.open_time and location.close_time:
            print(f"   开放时间: {location.open_time.strftime('%H:%M')} - "
                  f"{location.close_time.strftime('%H:%M')}")
            
            # 检查是否在时间窗口内
            if location.open_time <= arrival_time_only <= location.close_time:
                print(f"   ✓ 在开放时间内")
            else:
                print(f"   ✗ 不在开放时间内（需要等待）")
        
        # 显示到下一个地点的距离
        if i < len(solution.route) - 1:
            next_idx = solution.route[i + 1]
            distance = optimizer.get_distance_matrix().get_distance(loc_idx, next_idx)
            travel_time = optimizer.get_distance_matrix().get_travel_time(
                loc_idx, next_idx, optimizer.avg_speed
            )
            print(f"   → 下一站距离: {distance:.2f} 公里, 预计时间: {travel_time:.1f} 分钟")


if __name__ == "__main__":
    main()

