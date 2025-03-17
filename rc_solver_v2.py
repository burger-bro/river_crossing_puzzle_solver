from collections import deque
import itertools

def generate_moves(state, objects, rowers, boat_capacity):
    n = len(objects)
    current_boat_side = state[-1]
    current_shore = [i for i in range(n) if state[i] == current_boat_side]
    subsets = []
    # 生成所有可能的子集
    for k in range(1, boat_capacity + 1):
        for subset in itertools.combinations(current_shore, k):
            if any(objects[idx] in rowers for idx in subset):
                subsets.append(subset)
    # 生成新状态
    moves = []
    for subset in subsets:
        new_state = list(state)
        for idx in subset:
            new_state[idx] = 1 - new_state[idx]  # 翻转对象位置
        new_state[-1] = 1 - new_state[-1]       # 翻转船的位置
        moves.append(tuple(new_state))
    return moves

def is_valid(state, conditions, objects):
    for condition in conditions:
        # 检查所有对象是否在同一岸
        obj_indices = [objects.index(obj) for obj in condition['objects']]
        positions = [state[idx] for idx in obj_indices]
        if len(set(positions)) != 1:
            continue
        side = positions[0]
        # 检查该岸是否有监管者
        unless_indices = [objects.index(obj) for obj in condition['unless']]
        if any(state[idx] == side for idx in unless_indices):
            continue
        return False  # 触发冲突条件
    return True

def solve(objects, rowers, boat_capacity, conditions):
    n = len(objects)
    initial_state = tuple([0] * n + [0])  # 初始状态
    target_state = tuple([1] * n + [1])   # 目标状态

    queue = deque([(initial_state, [])])
    solutions = []

    while queue:
        current_state, path = queue.popleft()
        if current_state == target_state:
            solutions.append(path)
            continue
        for new_state in generate_moves(current_state, objects, rowers, boat_capacity):
            if is_valid(new_state, conditions, objects):
                # 检查新状态是否在路径中出现过
                if not any(s == new_state for s, _ in path):
                    new_path = path + [(new_state, describe_move(current_state, new_state, objects))]
                    queue.append((new_state, new_path))
    return solutions


def describe_move(old_state, new_state, objects):
    moved = [obj for i, obj in enumerate(objects) if old_state[i] != new_state[i]]
    direction = 'right' if new_state[-1] == 1 else 'left'
    return f"bring {', '.join(moved)} to {direction}"




# 输入参数
objects = ['mother', 'father', 'brother', 'sister', 'stranger']
rowers = ['mother', 'father', 'brother', 'stranger']
boat_capacity = 2
conditions = [
    {'objects': ['mother', 'father'], 'unless': ['brother', 'sister', 'stranger']},
    {'objects': ['mother', 'brother'], 'unless': ['father', 'sister', 'stranger']},
    {'objects': ['mother', 'stranger'], 'unless': ['brother', 'sister', 'father']},
    {'objects': ['sister', 'brother'], 'unless': ['mother', 'father', 'stranger']},
    {'objects': ['sister', 'father'], 'unless': ['mother', 'brother', 'stranger']},
    {'objects': ['brother', 'stranger'], 'unless': ['sister', 'brother', 'father']},
]

# 求解
solutions = solve(objects, rowers, boat_capacity, conditions)

# 输出结果
for i, path in enumerate(solutions):
    print(f"Solutions {i + 1}:")
    for step in path:
        print(step[1])
    print()

exit(0)

# 输入参数
objects = ['farmer', 'wolf', 'sheep', 'cabbage']
rowers = ['farmer']
boat_capacity = 2
conditions = [
    {'objects': ['wolf', 'sheep'], 'unless': ['farmer']},
    {'objects': ['sheep', 'cabbage'], 'unless': ['farmer']}
]

# 求解
solutions = solve(objects, rowers, boat_capacity, conditions)

# 输出结果
for i, path in enumerate(solutions):
    print(f"Solutions {i + 1}:")
    for step in path:
        print(step[1])
    print()

