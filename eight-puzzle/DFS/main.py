class Tree(object):
    def __init__(self, val, depth=1):
        self.val = val
        self.depth = depth
        self.children = []

    def insert_kid(self, val, parent):
        children_val_queue = []
        node = self
        while node.val != parent:
            temp = []
            for i in range(len(node.children)):
                temp.append(node.children[i])
                children_val_queue = [*temp, *children_val_queue]
            node = children_val_queue.pop(0)
        else:
            if node.depth + 1 <= max_depth:
                temp_node = Tree(val, node.depth + 1)
                node.children.append(temp_node)
        return node.depth + 1

def make_list(curr_state):
    state_list = []
    for row in curr_state:
        for val in row:
            state_list.append(val)
    return state_list

def make_matrix(curr_state):
    matrix_state, state_row = [], []
    for i, num in enumerate(curr_state):
        state_row.append(num)
        if len(state_row) == size:
            matrix_state.append(state_row.copy())
            state_row.clear()
    return matrix_state

def zero_neighbours(curr_state):
    zero_neighbours_indexes = []
    state_list = make_list(curr_state)
    zero_index = state_list.index(0)
    for i in range(0, len(state_list)):
        distance = abs(zero_index - i)
        if distance == size:
            zero_neighbours_indexes.append(i)
        elif distance == 1:
            max_index = max(i, zero_index)
            if max_index % size != 0:
                zero_neighbours_indexes.append(i)
    return zero_index, zero_neighbours_indexes, state_list

def state_generator(curr_state, finish_state):
    zero_index, neighbours_indexes, state_list = zero_neighbours(curr_state)
    finish_state_list = make_list(finish_state)
    temp_state_list = state_list.copy()
    for index in neighbours_indexes:
        temp_state_list[index], temp_state_list[zero_index] = temp_state_list[zero_index], temp_state_list[index]
        yield temp_state_list
        if temp_state_list == finish_state_list:
            break
        temp_state_list = state_list.copy()

def make_state_tree(state_tree, state_level, parent_state):
    depth = 1
    for state in state_level:
        depth = state_tree.insert_kid(state, parent_state)
    return state_tree, depth

def eight_game_dfs(curr_state, finish_state):
    depth, state_num = 1, 1
    visited, queue = {}, []
    state_dict = {}
    state_tree = Tree(curr_state, depth)
    file.truncate(0)
    if curr_state == finish_state or depth > max_depth:
        return state_dict, visited
    else:
        while curr_state != finish_state:
            if curr_state in list(visited.values()):
                state_dict.update({state_num: curr_state})
                state_num += 1
            else:
                control_state, state_level = curr_state, []
                for gener_state in state_generator(curr_state, finish_state):
                    neighbour_gener_state = make_matrix(gener_state)
                    if neighbour_gener_state not in list(visited.values()):
                        state_level.append(neighbour_gener_state)
                if len(state_level) > 0:
                    state_tree, depth = make_state_tree(state_tree, state_level, curr_state)
                state_dict.update({state_num: curr_state})
                if curr_state not in list(visited.values()):
                    visited.update({state_num: curr_state})
                    file.write(f"{state_num}: {curr_state}\n")
                state_num += 1
                temp = []
                for gen_state in state_generator(curr_state, finish_state):
                    neighbour_gen_state = make_matrix(gen_state)
                    if depth > max_depth:
                        break
                    else:
                        temp.append(neighbour_gen_state)
                    control_state = neighbour_gen_state
                queue = [*temp, *queue]
            if control_state == finish_state:
                state_dict.update({state_num: control_state})
                if control_state not in list(visited.values()):
                    visited.update({state_num: control_state})
                    file.write(f"{state_num}: {control_state}\n")
                print("Рішення знайдено!\n"
                      f"Кінцевий стан:")
                for state in control_state:
                    print(state)
                print(f"Глибина пошуку: {depth}; "
                      f"Кількість згенерованих станів: {len(state_dict)}, "
                      f"занесених в базу станів: {len(visited)}, "
                      f"відкинутих станів: {len(state_dict) - len(visited)}")
                break
            elif queue:
                curr_state = queue.pop(0)
            else:
                if depth > max_depth:
                    print(f"Для заданої глибини - {depth - 1} рішення не знайдено.\n"
                          f"Кількість згенерованих станів: {len(state_dict)}, "
                          f"занесених в базу станів: {len(visited)}, "
                          f"відкинутих станів: {len(state_dict) - len(visited)}")
                    break
                else:
                    print("Для заданих умов рішення задачі не існує.\n"
                          f"Кількість згенерованих станів: {len(state_dict)}, "
                          f"занесених в базу станів: {len(visited)}, "
                          f"відкинутих станів: {len(state_dict) - len(visited)}")
                    break
        return state_dict, visited

if __name__ == '__main__':
    start = []
    size = int(input("Розмірність таблиці: "))
    print("Початковий стан: ")
    for j in range(size):
        start.append([int(value) for value in input().split()])
    finish = []
    print("Кінцевий стан: ")
    for j in range(size):
        finish.append([int(value) for value in input().split()])
    max_depth = int(input("Максимальна глибина пошуку ∈(1 - inf); -1 = inf: "))
    if max_depth == -1:
        max_depth = float("inf")
    file = open("states.txt", "a")
    all_states, base_states = eight_game_dfs(start, finish)
    choice = input("\nВиберіть дію: 1 - вивести перший стан; 0 - вийти: ")
    pos = 0
    while choice:
        if choice == "1":
            if pos < len(base_states):
                print(f"Стан №{list(base_states.keys())[pos]}:")
                for staterow in list(base_states.values())[pos]:
                    print(staterow)
                pos += 1
            else:
                print("Немає більше станів!")
                break
            choice = input("\nВиберіть дію: 1 - вивести наступний стан; 0 - вийти: ")
        elif choice == "0":
            break
        else:
            choice = input("\nНеправильний ввід!\n"
                           "Виберіть дію: 1 - вивести наступний стан; 0 - вийти: ")
    file.close()
