
BLOCKS = (
    "\u258F",
    "\u258E",
    "\u258D",
    "\u258C",
    "\u258B",
    "\u258A",
    "\u2589",
    "\u2588"
)

class ProgressBar:
    """Naive progress bar which assumes unique access to stdout on a single line"""

    def __init__(self, size_bytes: int, width: int):
        if not isinstance(size_bytes, int):
            raise TypeError("size_bytes must be an integer")
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        if size_bytes < 1:
            raise ValueError("size_bytes must be positive")
        if width < 1:
            raise ValueError("width must be positive")
        
        self.size_bytes = size_bytes
        self.width = width

        # import shutil
        # terminal_size = shutil.get_terminal_size((-1,-1))
        # print(f"{terminal_size=}")

    def __enter__(self):
        print("\x1b[?25l", end="", flush=True) # hide cursor
        return self

    def __exit__(self, exc_type, exc, tb):
        print("\x1b[?25h") # show cursor and print newline

    def update(self, n_bytes: int):
        if not isinstance(n_bytes, int):
            raise TypeError("n_bytes must be an integer")
        if n_bytes < 1:
            raise ValueError("n_bytes must be positive")
        
        progress = n_bytes / self.size_bytes

        n_full_blocks = int(progress * self.width)
        blocks = BLOCKS[7] * n_full_blocks
        partial_block_size = int(progress * self.width * 8) % 8
        if partial_block_size > 0:
            blocks += BLOCKS[partial_block_size - 1]
        
        display = "\r|{:{width}s}| {:.2f}%".format(blocks, 100 * progress, width=self.width)
        print(display, end="", flush=True)



if __name__ == "__main__":
    import time

    bar = ProgressBar(100, 30)
    print("EXAMPLE:\x1b[?25l")
    for i in range(1, 101):
        bar.update(i)
        time.sleep(0.05)
    print("\x1b[?25h")
