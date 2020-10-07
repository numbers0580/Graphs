
def earliest_ancestor(ancestors, starting_node):
    # GENERAL NOTE:
    # I went through this completed code to rename all non-parameter variables as the genus or species of VERY early hominids for funsies.
    
    # According to test file:
    # ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    # lucy = selectedNode
    lucy = None

    for ramidus in ancestors:
        # ramidus = [1, 3], then ramidus = [2, 3], etc
        # in 1st test, looking for ramidus = [10, 1], starting_node = 1, return 10
        if starting_node is ramidus[1]:
            # both = [10, 1]
            lucy = ramidus
            break

    # if no matching nodes found in the above for-loop
    if lucy is None:
        return -1

    # paranthropus = visited
    paranthropus = set()
    ardipithecus = []
    ardipithecus.insert(0, lucy)

    while len(ardipithecus) > 0:
        # boisei = temp
        boisei = ardipithecus.pop(0)
        afarenses = boisei[0] # afarenses = 1 in [1, 3], 2 in [2, 3], ... 10 in [10, 1]

        if boisei not in paranthropus:
            # visited.add(temp)
            paranthropus.add(boisei)

            for australopithecus in ancestors:
                # Check if the 2nd position of this node matches the 1st position of popped node
                if australopithecus[1] is afarenses:
                    # Found it! Append to main stack to continue the while-loop
                    ardipithecus.append(australopithecus)
                    break

    # Out of while-loop, meaning no further parent nodes found. Return parent-most value
    return afarenses
