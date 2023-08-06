def partition(rows, partition_size):
    start = 0
    partitions = []
    while start < rows:
        end = start + partition_size - 1
        if end > rows:
            end = rows - 1
        partitions.append({"start": start, "end": end})
        start += partition_size
    return partitions