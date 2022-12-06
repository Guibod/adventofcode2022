class DataStreamBuffer:
    def __init__(self, string):
        self.input = string

    def first_marker_after(self, size=4):
        for i, b in enumerate(self.get_buffers(size)):
            if len(set(b)) == len(b):
                return i + size
        return None

    def get_buffers(self, size):
        if size > len(self.input):
            raise ValueError
        for i in range(0, len(self.input) - size + 1):
            yield list(self.input[i:i+size])


test_buffer = DataStreamBuffer("abcdefghijkl")
buffers = list(test_buffer.get_buffers(4))
assert len(buffers) == 9
assert buffers[0] == ["a", "b", "c", "d"]
assert buffers[1] == ["b", "c", "d", "e"]
assert buffers[8] == ["i", "j", "k", "l"]

assert DataStreamBuffer("mjqjpqmgbljsphdztnvjfqwrcgsmlb").first_marker_after() == 7
assert DataStreamBuffer("bvwbjplbgvbhsrlpgdmjqwftvncz").first_marker_after() == 5
assert DataStreamBuffer("nppdvjthqldpwncqszvftbrmjlhg").first_marker_after() == 6
assert DataStreamBuffer("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg").first_marker_after() == 10
assert DataStreamBuffer("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw").first_marker_after() == 11

with open("input.txt", encoding="utf-8") as file:
    buffer = file.readline()
ds = DataStreamBuffer(buffer)

print(f"Datastream buffer needed {ds.first_marker_after()} characters to be "
      f"processed before the first start-of-packet marker was detected")
