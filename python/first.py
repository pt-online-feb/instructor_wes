# print("20" + str(20))

# console.log("20" + 20);

my_tuple = (1, 2, 3, 4)
my_list = [1, 2, 3, 4]
# list = []
# print(my_tuple)

# nested = [1, [1, 2, 3], 3, 4]

# for item in nested:
#     if isinstance(item, list):
#         item[1] = 100
# print(nested)

other_list = ["first", "second", "third", "fourth"]
for item in other_list:
    if item == "second":
        item = "this should change"
# print(other_list)
# print("hello")

# for (var i = 0; i < other_list.length; i++) {
#     console.log(other_list[i]);
# }
# console.log(other_list.length);

for i in range(0, len(other_list), 2):
    if other_list[i] == "second":
        other_list[i] = "changed"
    # print(other_list[i])
# print(other_list)


# starts at high num
# counts down to low num
# prints only multiples of mult
def flexible_countdown(high_num, low_num, mult):
    for idx in range(high_num, low_num - 1, -1):
        if idx % mult == 0:
            print(idx)

# flexible_countdown(9, 3, 2) # 9, 6, 3

my_int = 10
my_float = 10.1

test = [1, 2, 3, 4, 5]
test_two = [1, 2, 3, 4, 5, 6]
def reverse_list(lst):
    halfway = int(len(lst) / 2)
    for i in range(halfway):
        # temp = lst[i]
        # lst[i] = lst[len(lst) - 1 - i]
        # lst[len(lst) - 1 - i] = temp
        
        lst[i], lst[len(lst) - 1 - i] = lst[len(lst) - 1 - i], lst[i]
    return lst

print(reverse_list(test))
print(reverse_list(test_two))
