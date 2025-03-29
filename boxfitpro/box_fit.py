from itertools import permutations

def box_it(dims, boxes):
    res = []
    alpha = float('inf')
    closest_box = None
    min_deficit = float('inf')

    # Calculate cubic volume for the item
    item_volume = dims[0] * dims[1] * dims[2]

    # Generate all possible orientations for the item
    rotations = list(permutations(dims))

    for x in boxes:
        box_volume = x[0] * x[1] * x[2]

        # Check all possible item rotations
        fits = any(
            rot[0] <= x[0] and rot[1] <= x[1] and rot[2] <= x[2]
            for rot in rotations
        )

        if fits:
            if box_volume < alpha:
                alpha = box_volume
                res = x
        else:
            # Calculate the volume deficit for closest box logic
            deficit = item_volume - box_volume
            if deficit < min_deficit:
                min_deficit = deficit
                closest_box = x

    if len(res) == 0:
        return 'No box fits', closest_box
    return res, None


# Sample list of boxes (length, width, height)
# available_boxes = [
#     (10, 10, 10),
#     (15, 15, 15),
#     (20, 20, 20),
#     (25, 25, 25),
#     (30, 30, 30)
# ]