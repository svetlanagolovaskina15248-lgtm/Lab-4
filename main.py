def knapsack(weights, values, capacity, n): #размер пр., очки пр., вместимость рюкзака, кол-во пр.

    #таблица DP (n+1)*(capacity+1)
    #dp[i][w] максимальные очки для первых i пр. и вместимости w
    dp = [[0 for x in range(capacity + 1)] for x in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w: #пр. помещается 
                dp[i][w] = max(dp[i-1][w], 
                              dp[i-1][w - weights[i-1]] + values[i-1]) #макс. очки для ост. места + очки пр.
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp

def get_selected_items(dp, weights, values, capacity, n, items):

    w = capacity
    selected = [] #выбранные пр.
    total_value = dp[n][capacity]
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]: #значение изменилось, то пр. взят
            selected.append(items[i-1])
            w -= weights[i-1]  #уменьшение вместимости р.
    
    return selected, total_value

#дано
capacity = 8  #2*4
start_points = 15
disease = "нет"

#словарь пр.
items_dict = {
    'r': (3, 25), 'p': (2, 15), 'a': (2, 15), 'm': (2, 20),
    'i': (1, 5), 'k': (1, 15), 'x': (3, 20), 't': (1, 25),
    'f': (1, 15), 'd': (1, 10), 's': (2, 20), 'c': (2, 20)
}

required_items = []
if disease == "астма":
    required_items = ['i']
elif disease == "паранойя":
    required_items = ['d']

items_list = list(items_dict.keys())  #список ключей из словаря
weights = [items_dict[item][0] for item in items_list]
values = [items_dict[item][1] for item in items_list]
n = len(items_list)

dp_table = knapsack(weights, values, capacity, n)
selected, items_value = get_selected_items(dp_table, weights, values, capacity, n, items_list)

#проверка на обязательные пр.
if required_items:
    missing_required = [req for req in required_items if req not in selected]
    if missing_required:
        temp_selected = []
        temp_capacity = capacity
        
        #доб. обязательные пр.
        for req in required_items:
            if req in items_dict and items_dict[req][0] <= temp_capacity:
                temp_selected.append(req)
                temp_capacity -= items_dict[req][0]
        
        for item in selected:
            if item not in required_items and items_dict[item][0] <= temp_capacity: #пр. необязательный и помещается
                temp_selected.append(item)
                temp_capacity -= items_dict[item][0]
        
        selected = temp_selected

#инвентарь
backpack_display = []
used_space = 0

for item in selected:
    size = items_dict[item][0]
    for x in range(size): #доб. пр. нужное колво раз
        backpack_display.append(item)
    used_space += size

#2*4
grid = []
for i in range(0, len(backpack_display), 4):
    row = backpack_display[i:i+4]
    grid.append(row)

#итоговые очки
total_points = start_points
for item in items_dict:
    if item in selected:
        total_points += items_dict[item][1]  #пр. взят
    else:
        total_points -= items_dict[item][1]  #пр. отсутствует

#рез.
if total_points > 0:
    for row in grid:
        formatted_row = ", ".join(f"[{item}]" for item in row)
        print(formatted_row)
else:
    print("Итоговый счет отрицательный")

print(f"\nИтоговые очки выживания: {total_points}")
