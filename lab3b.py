import sys
import csv
from collections import defaultdict


if len(sys.argv) != 2:
    sys.stderr.write("The only argument should be the csv file.\n")
    exit(1)

file_path = sys.argv[1]

num_block = 0
num_inode = 0
block_size = 0
inode_size = 0
block_per_group = 0
inode_per_group = 0
first_non_reserved_inode = 0

free_list = defaultdict(int)
reference_list = defaultdict(int)
free_inode_list = defaultdict(int)
inode_reference_list = defaultdict(int)
dir_counts = defaultdict(int)

with open(file_path, "r") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if row[0] == 'SUPERBLOCK':
            num_block = int(row[1])
            num_inode = int(row[2])
            block_size = int(row[3])
            inode_size = int(row[4])
            block_per_group = int(row[5])
            inode_per_group = int(row[6])
            first_non_reserved_inode = int(row[7])
        if row[0] == 'BFREE':
            free_list[row[1]] += 1
        if row[0] == 'INODE':
            for each in row[12:]:
                if (int(each) != 0):
                    reference_list[each] += 1
            inode_reference_list[row[1]] += 1
        if row[0] == 'INDIRECT':
            reference_list[row[5]] += 1
        if row[0] == 'IFREE':
            free_inode_list[row[1]] += 1
        if row[0] == 'DIRENT':
            dir_counts[row[3]] += 1

with open(file_path, "r") as f:
    reader = csv.reader(f, delimiter=',')
    reserved = int(4 + num_inode / 8)
    for each in range(reserved + 1, num_block):
        if str(each) not in free_list and str(each) not in reference_list:
            print(f"UNREFERENCED BLOCK {each}")

    for each in range(first_non_reserved_inode, num_inode + 1):
        if str(each) not in free_inode_list and str(each) not in inode_reference_list:
            print(f"UNALLOCATED INODE {each} NOT ON FREELIST")
    for each in range(1, num_inode + 1):
        if str(each) in free_inode_list and str(each) in inode_reference_list:
            print(f"ALLOCATED INODE {each} ON FREELIST")

    for row in reader:
        if row[0] == 'INODE':

            for i, each_block in enumerate(row[12:24]):
                if int(each_block) < 0 or int(each_block) > num_block:
                    print(f"INVALID BLOCK {each_block} IN INODE {row[1]} AT OFFSET {i}")
                if int(each_block) > 0 and int(each_block) < reserved:
                    print(f"RESERVED BLOCK {each_block} IN INODE {row[1]} AT OFFSET {i}")

            for i, each_block in enumerate(row[12:]):
                if int(each_block) != 0 :
                    if each_block in free_list and each_block in reference_list:
                        if i == 13:
                            print(f"ALLOCATED INDIRECT BLOCK {each_block} ON FREELIST")
                        elif i == 14:
                            print(f"ALLOCATED DOUBLE INDIRECT BLOCK {each_block} ON FREELIST")
                        elif i == 15:
                            print(f"ALLOCATED TRIPLE INDIRECT BLOCK {each_block} ON FREELIST")
                        else:
                            print(f"ALLOCATED BLOCK {each_block} ON FREELIST")
                    elif reference_list[each_block] > 1:
                        if i == 13:
                            print(f"DUPLICATE INDIRECT BLOCK {each_block} IN INODE {row[1]} AT OFFSET 12")
                        elif i == 14:
                            print(f"DUPLICATE DOUBLE INDIRECT BLOCK {each_block} IN INODE {row[1]} AT OFFSET 268")
                        elif i == 15:
                            print(f"DUPLICATE TRIPLE INDIRECT BLOCK {each_block} IN INODE {row[1]} AT OFFSET 65804")
                        else:
                            print(f"DUPLICATE BLOCK {each_block} IN INODE {row[1]} AT OFFSET {i}")

            if int(row[24]) < 0 or int(row[24]) > num_block:
                print(f"INVALID INDIRECT BLOCK {row[24]} IN INODE {row[1]} AT OFFSET 12")
            if int(row[24]) > 0 and int(row[24]) < reserved:
                print(f"RESERVED INDIRECT BLOCK {row[24]} IN NODE {row[1]} AT OFFSET 12")
            if int(row[25]) < 0 or int(row[25])> num_block:
                print(f"INVALID DOUBLE INDIRECT BLOCK {row[25]} IN INODE {row[1]} AT OFFSET 268")
            if int(row[25]) > 0 and int(row[25]) < reserved:
                print(f"RESERVED DOUBLE INDIRECT BLOCK {row[25]} IN NODE {row[1]} AT OFFSET 268")
            if int(row[26]) < 0 or int(row[26])> num_block:
                print(f"INVALID TRIPLE INDIRECT BLOCK {row[26]} IN INODE {row[1]} AT OFFSET 65804")
            if int(row[26]) > 0 and int(row[26]) < reserved:
                print(f"RESERVED TRIPLE INDIRECT BLOCK {row[26]} IN NODE {row[1]} AT OFFSET 65804")

            if dir_counts[row[1]] != int(row[6]):
                print(f"INODE {row[1]} HAS {dir_counts[row[1]]} LINKS BUT LINKCOUNT IS {row[6]}")


        if row[0] == 'INDIRECT':
            level = "INDIRECT"
            if(int(row[2]) == 2):
                level = "DOUBLE INDIRECT"
            elif(int(row[2]) == 3):
                level = "TRIPLE INDIRECT"
            if int(row[5]) < 0 or int(row[5]) > num_block:
                print(f"INVALID {level} BLOCK {row[5]} IN INODE {row[1]} AT OFFSET {row[3]}")
            if int(row[5]) > 0 and int(row[5]) < reserved:
                print(f"RESERVED {level} BLOCK {row[5]} IN INODE {row[1]} AT OFFSET {row[3]}")
            if reference_list[row[5]] > 1:
                print(f"DUPLICATE {level} BLOCK {row[5]} IN INODE {row[1]} AT OFFSET {row[3]}")
