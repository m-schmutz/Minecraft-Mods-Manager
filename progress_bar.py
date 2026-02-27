

class ProgressBar:
    """Naive progress bar which assumes unique access to stdout on a single line"""

    BLOCKS = (
        "\u258F",
        "\u258E",
        "\u258D",
        "\u258C",
        "\u258B",
        "\u258A",
        "\u2589",
        "\u2588")

    @staticmethod
    def _hex_to_rgb_ansi(hex: int):
        if not isinstance(hex, int):
            raise TypeError("hex must be an integer")
        
        s = "{:06x}".format(hex)
        
        b = int(s[-2:], base=16)
        g = int(s[-4:-2], base=16)
        r = int(s[-6:-4], base=16)

        return f"\x1b[38;2;{r};{g};{b}m"

    def __init__(self, size_bytes: int, width: int, color_hex: int = None):
        if not isinstance(size_bytes, int):
            raise TypeError("size_bytes must be an integer")
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        if not isinstance(color_hex, int):
            raise TypeError("color_hex must be an integer")
        
        if size_bytes < 1:
            raise ValueError("size_bytes must be positive")
        if width < 1:
            raise ValueError("width must be positive")
        
        self.size_bytes = size_bytes
        self.width = width
        self.color_ansi = None if color_hex is None else ProgressBar._hex_to_rgb_ansi(color_hex)

        # import shutil
        # terminal_size = shutil.get_terminal_size((-1,-1))
        # print(f"{terminal_size=}")

    def __enter__(self):
        print("\x1b[?25l", end="", flush=True) # hide cursor
        return self

    def __exit__(self, exc_type, exc, tb):
        print("\x1b[?25h") # show cursor and print newline
    
    def _make_bar(self, progress: float):
        n_full_blocks = int(progress * self.width)
        blocks = ProgressBar.BLOCKS[7] * n_full_blocks
        partial_block_size = int(progress * self.width * 8) % 8
        if partial_block_size > 0:
            blocks += ProgressBar.BLOCKS[partial_block_size - 1]

        bar = ""
        if self.color_ansi is not None:
            bar += self.color_ansi
        
        bar += "{:{width}s}".format(blocks, width=self.width)
        
        if self.color_ansi is not None:
            bar += "\x1b[0m"

        return bar

    def update(self, n_bytes: int):
        if not isinstance(n_bytes, int):
            raise TypeError("n_bytes must be an integer")
        if n_bytes < 1:
            raise ValueError("n_bytes must be positive")
        
        progress = n_bytes / self.size_bytes
        display = "\r|{}| {:.2f}%".format(self._make_bar(progress), 100 * progress)

        print(display, end="", flush=True)



if __name__ == "__main__":
    import time
    
    bar = ProgressBar(255, 30, color_hex=0xffff00)
    print("EXAMPLE:\x1b[?25l")
    for i in range(1, 256):
        bar.update(i)
        time.sleep(0.02)
    print("\x1b[?25h")

    # print(ProgressBar._hex_to_rgb_ansi(0x000000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0x110000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0x220000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0x330000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0x440000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0x550000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0x660000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0x770000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0x880000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0x990000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0xaa0000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0xbb0000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0xcc0000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0xdd0000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0xee0000) + "hello" + "\x1b[0m")
    # print(ProgressBar._hex_to_rgb_ansi(0xff0000) + "hello" + "\x1b[0m")
