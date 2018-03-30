def dithered_curve(size, factor=1, scale=1.0):
    def func(idx):
        progress = float(idx) / (size - 1)
        return (1 - (1 - progress) ** (2 ** -factor)) ** (2 ** factor)
    acc = 1
    for idx in xrange(size):
        acc += func(idx) * scale
        if acc >= 0.5:
            yield 1
            acc -= 1
        else:
            yield 0

def prune(items, curve=1, scale=1.0):
    selectors = dithered_curve(len(items), factor=curve, scale=scale)
    for item in compress(items, selectors):
        yield item
