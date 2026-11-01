from itertools import islice


def chunked_even(iterable, n):
    """Break *iterable* into lists of approximately length *n*.
    Items are distributed such the lengths of the lists differ by at most
    1 item.

    >>> iterable = [1, 2, 3, 4, 5, 6, 7]
    >>> n = 3
    >>> list(chunked_even(iterable, n))  # List lengths: 3, 2, 2
    [[1, 2, 3], [4, 5], [6, 7]]
    >>> list(chunked(iterable, n))  # List lengths: 3, 3, 1
    [[1, 2, 3], [4, 5, 6], [7]]

    """
    iterator = iter(iterable)

    # Initialize a buffer to process the chunks while keeping
    # some back to fill any underfilled chunks
    min_buffer = (n - 1) * (n - 2)
    buffer = list(islice(iterator, min_buffer))

    # Append items until we have a completed chunk
    for _ in islice(map(buffer.append, iterator), n, None, n):
        yield buffer[:n]
        del buffer[:n]

    # Check if any chunks need addition processing
    if not buffer:
        return
    length = len(buffer)

    # Chunks are either size `full_size <= n` or `partial_size = full_size - 1`
    q, r = divmod(length, n)
    num_lists = q + (1 if r > 0 else 0)
    q, r = divmod(length, num_lists)
    full_size = q + (1 if r > 0 else 0)
    partial_size = full_size - 1
    num_full = length - partial_size * num_lists

    # Yield chunks of full size
    partial_start_idx = num_full * full_size
    if full_size > 0:
        for i in range(0, partial_start_idx, full_size):
            yield buffer[i : i + full_size]

    # Yield chunks of partial size
    if partial_size > 0:
        for i in range(partial_start_idx, length, partial_size):
            yield buffer[i : i + partial_size]
