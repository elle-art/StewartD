def read_lines(filepath, encoding='utf-8'):
    """
    Yield lines from a file one at a time.
    - Strip whitespace from each line
    - Skip empty lines
    - Handle encoding errors gracefully
    
    Usage:
        for line in read_lines('large_file.txt'):
            process(line)
    """
    with open(filepath, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line: # empty lines are False
                yield line.strip()

def batch(iterable, size):
    """
    Yield items in batches of the specified size.
    
    Usage:
        list(batch([1,2,3,4,5,6,7], 3))
        # [[1,2,3], [4,5,6], [7]]
    """
    while iterable:
        my_batch = []
        for _ in range(size):
            if not iterable:
                break
            my_batch.append(iterable.pop(0))
        yield my_batch

def filter_by(iterable, predicate):
    """
    Yield items that match the predicate.
    
    Usage:
        evens = filter_by(range(10), lambda x: x % 2 == 0)
        list(evens)  # [0, 2, 4, 6, 8]
    """
    return (x for x in iterable if predicate(x))