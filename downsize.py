N = 8_000_000 # 12_603_976

# with open("UWRL_river_velocimetry_dataset.csv", "r") as f:
#     file = f.readlines()

# # print(len(file))
# print("X")
# i = 0
# with open("UWRL_river_velocimetry_dataset_NEW.csv", "w") as f:
#     for line in file:
#         f.write(line)
            
#         i += 1
#         if i > N:
#             break   

print("X")
with open("UWRL_river_velocimetry_dataset_angle_variance.csv", "r") as f:
    file = f.readlines()

# print(len(file))
print("X")

i = 0
with open("UWRL_river_velocimetry_dataset_angle_variance_NEW.csv", "w") as f:
    for line in file:
        f.write(line)
            
        i += 1
        if i > N:
            break   

print("X")