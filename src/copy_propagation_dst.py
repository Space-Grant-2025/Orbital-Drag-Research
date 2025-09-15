import csv
import os
import shutil

weak_dst_min, weak_dst_max = -50, -30
mod_dst_min, mod_dst_max = -100, -50
# site says -300, but -400 for safety
strong_dst_min, strong_dst_max = -400, -100

def get_dst(id):
    with open("../data/epoch_masterlist.csv") as f:
        reader = csv.reader(f)
        # pass over headers
        next(reader)

        for row in reader:
            if int(row[0]) == id:
                dst = float(row[11])
                return dst

def get_id_list(min_dst, max_dst):
    id_list = []
    with open("../data/starlink_reentries_list.txt") as f:
        next(f)
        for line in f:
            id = int(line.strip())
            dst = get_dst(id)
            if min_dst <= dst <= max_dst:
                id_list.append(id)
    return id_list

def main():
    id_list = get_id_list(strong_dst_min, strong_dst_max)

    src_dir = "../data/starlink_reentries_2020_2025/propagations/"
    new_dir = "../../../../../Desktop/Propagations/strong-dst/"

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    for id in id_list:
        shutil.copy(src_dir + f"propagation_{id}.csv", new_dir + f"propagation_{id}.csv")
        print(id)

main()
