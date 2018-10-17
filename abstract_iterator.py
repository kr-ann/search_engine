def abstract_iterator(list_of_lists):
    """
    Simultaneous sorting.
    Takes an iterable of iterables and yields elements in ascending order.
    """

    # list_of_iter_lists contains iterators for each list in list_of_lists
    list_of_iter_lists = []
    try:
        for sorted_list in list_of_lists:
            list_of_iter_lists.append(iter(sorted_list))
    except TypeError:
        # is raise if either outer "list" or inner "lists" are not iterable
        raise TypeError("The input parapeter must be iterable.")        

    first_elements = []
    for iter_list in list_of_iter_lists:
        first_elements.append(next(iter_list)) # first elements in each iter_list

    while len(first_elements)>0: # if len = 0 then all ietrators have ended
        min_el = min(first_elements)

        # proceed to the next element in the list from which we took the min_el
        min_ind = first_elements.index(min_el)
        try:
            first_elements[min_ind] = next(list_of_iter_lists[min_ind])
        except StopIteration:
            first_elements.pop(min_ind)
            list_of_iter_lists.pop(min_ind)
        yield min_el


        """for i,element in enumerate(first_elements):
            if element == min_el:
                try: # и то же самое"""
