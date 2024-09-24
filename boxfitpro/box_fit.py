def box_it(dims, boxes):
    res = []
    alpha = float('inf')
    for x in boxes:
        if x[0] >= dims[0] and x[1] >= dims[1] and x[2] >= dims[2]:
            var = sum(x)
            if var <= alpha:
                alpha = var
                res = x
    if len(res) == 0:
        return 'No box fits'
    return res

# Sample list of boxes (length, width, height)
# available_boxes = [
#     (10, 10, 10),
#     (15, 15, 15),
#     (20, 20, 20),
#     (25, 25, 25),
#     (30, 30, 30)
# ]