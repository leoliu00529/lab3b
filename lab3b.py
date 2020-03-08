import sys
import csv

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

with open(file_path, "r") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if row[0] == 'INODE':
            for i, each_block in enumerate(row[12:24]):
                if int(each_block) < 0 or int(each_block) > num_block:
                    print(f"INVALID BLOCK {each_block} IN INODE {row[1]} AT OFFSET {i}")









