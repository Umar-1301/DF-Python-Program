import pytsk3
import json
import hashlib


def main():
    # Get user input for forensic image file
    image_file = input("Enter the forensic image file: ")

    # Open the forensic image using pytsk3
    try:
        image = pytsk3.Img_Info(image_file)
    except:
        print("Error: Failed to open image file.")
        return

    # Get the partition layout (MBR or GPT)
    disk = pytsk3.Volume_Info(image)

    if disk.info.vstype == pytsk3.TSK_VS_TYPE_DOS:
        print("Layout: MBR\n")
    else:
        print("Layout: GPT\n")
        disk.info.block_size
    print(f'Block size: {disk.info.block_size}')
    print(f'Sector size: {image.get_size()}')
    print(f'Total size of sector: {image.get_size() / disk.info.block_size}')

    for part in disk:
        if part.len > 20971520:
            if part.desc == "Unallocated Space":
                pass
            else:
                print("Partition Layout: ", part.desc)

    while True:
        # Print menu
        print("\nMenu:")
        print("1. Discover partitions")
        print("2. Select partition")
        print("3. Create report")
        print("4. Exit")

        # Get user input for menu choice
        choice = input("Enter your choice: ")

        # Discover partitions
        if choice == "1":
            discover_partitions(image, disk)

        # Select partition
        elif choice == "2":
            select_partition(image, disk)

        # Create report
        elif choice == "3":
            create_report(image, disk)

        # Exit
        elif choice == "4":
            return


def discover_partitions(image, disk):
    # Create table header
    print("\nPartition Table:")
    print(
        "{:<20}{:<20}{:<20}{:<20}{:<20}".format("Partition Number", "File System", "Start Sector", "Number of Sectors",
                                                "Total Allocated Space"))
    print("-" * 100)

    counter = 1

    # Print partition information
    for part in disk:
        if part.desc == "Unallocated Space":
            pass
        else:
            print("{:<20}{:<20}{:<20}{:<20}{:<20}".format(counter, part.desc.decode("ascii"), part.start, part.len,
                                                          part.len * 512))
        counter += 1


def select_partition(image, disk):
    # Get user input for partition number
    part_num = int(input("Enter the partition number: "))

    part_offsets = []

    for partition in disk:
        part_offsets.append(partition.start)

    # Open the selected partition
    try:
        part = pytsk3.FS_Info(image, part_offsets[part_num - 1] * disk.info.block_size)
    except:
        print("Error: Failed to open partition.")
        return

    # Ask user for hash value
    user_hash = input("Enter the MD5 hash to search: ")

    # Print partition details
    print("\nPartition Details:")
    print("{:<20}{:<28}{:<16}{:<24}".format("Item Number", "File Name", "Is File", "MD5 Hash"))
    print("-" * 80)

    counter = 1

    root_map = part.open_dir(inode=part.info.root_inum)

    for file in root_map:
        if file.info.meta != None:
            if file.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                file_type = 'Directory'
                print("{:<20}{:<28}{:<16}".format(counter, file.info.name.name.decode("ascii"), file_type))
            else:
                file_type = 'File'

                if file.info.meta.size > 0:
                    # Compare hash of files to user's hash
                    md5_hash_value = hashlib.md5()
                    read_bytes = file.info.meta.size
                    data = file.read_random(0, read_bytes)
                    md5_hash_value.update(data)

                    print("{:<20}{:<28}{:<16}{:<24}".format(counter, file.info.name.name.decode("ascii"), file_type,
                                                            md5_hash_value.hexdigest()))
                    if md5_hash_value.hexdigest().upper() == user_hash.upper():
                        print("MD5 hash match found for file above")

        counter += 1


def create_report(image, disk):
    # Get user input for report file name
    report_file = input("Enter the report file name: ")

    # Create data structure for report
    report = {"partition_table": [], "partition_details": []}

    # Add partition information to report
    counter = 1
    for part in disk:
        if part.desc == "Unallocated Space":
            pass
        else:
            report["partition_table"].append(
                {"Partition Number": counter, "File System": part.desc.decode("ascii"), "Start Sector": part.start,
                 "Number of Sectors": part.len, "Total Allocated Space": part.len * 512})
            counter += 1

    # Open the selected partition
    part_num = int(input("Enter the partition number: "))
    part_offsets = []

    for partition in disk:
        part_offsets.append(partition.start)

    try:
        part = pytsk3.FS_Info(image, part_offsets[part_num - 1] * disk.info.block_size)
    except:
        print("Error: Failed to open partition.")
        return

    # Print partition details
    print("\nPartitionDetails:")
    print("{:<20}{:<28}{:<16}{:<24}".format("Item Number", "File Name", "Is File", "MD5 Hash"))
    print("-" * 80)

    counter = 1

    root_map = part.open_dir(inode=part.info.root_inum)

    for file in root_map:
        if file.info.meta != None:
            if file.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                file_type = 'Directory'
                print("{:<20}{:<28}{:<16}".format(counter, file.info.name.name.decode("ascii"), file_type))
                report["partition_details"].append(
                    {"Item Number": counter, "File Name": file.info.name.name.decode("ascii"), "Is File": file_type,
                     "MD5 Hash": "N/A"})
            else:
                file_type = 'File'

                if file.info.meta.size > 0:
                    # Compare hash of files to user's hash
                    md5_hash_value = hashlib.md5()
                    read_bytes = file.info.meta.size
                    data = file.read_random(0, read_bytes)
                    md5_hash_value.update(data)
                    print("{:<20}{:<28}{:<16}{:<24}".format(counter, file.info.name.name.decode("ascii"), file_type,
                                                            md5_hash_value.hexdigest()))
                    report["partition_details"].append(
                        {"Item Number": counter, "File Name": file.info.name.name.decode("ascii"), "Is File": file_type,
                         "MD5 Hash": md5_hash_value.hexdigest()})
                else:
                    print("{:<20}{:<28}{:<16}{:<24}".format(counter, file.info.name.name.decode("ascii"), file_type,
                                                            "N/A"))
                    report["partition_details"].append(
                        {"Item Number": counter, "File Name": file.info.name.name.decode("ascii"), "Is File": file_type,
                         "MD5 Hash": "N/A"})
    counter += 1

    # Write report to json file
    with open(report_file + '.json', "w") as f:
        json.dump(report, f)
    print("Report created successfully!")


if __name__ == "__main__":
    main()
