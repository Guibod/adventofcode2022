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

assert DataStreamBuffer("mjqjpqmgbljsphdztnvjfqwrcgsmlb").first_marker_after(4) == 7
assert DataStreamBuffer("mjqjpqmgbljsphdztnvjfqwrcgsmlb").first_marker_after(14) == 19
assert DataStreamBuffer("bvwbjplbgvbhsrlpgdmjqwftvncz").first_marker_after(4) == 5
assert DataStreamBuffer("bvwbjplbgvbhsrlpgdmjqwftvncz").first_marker_after(14) == 23
assert DataStreamBuffer("nppdvjthqldpwncqszvftbrmjlhg").first_marker_after(4) == 6
assert DataStreamBuffer("nppdvjthqldpwncqszvftbrmjlhg").first_marker_after(14) == 23
assert DataStreamBuffer("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg").first_marker_after(4) == 10
assert DataStreamBuffer("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg").first_marker_after(14) == 29
assert DataStreamBuffer("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw").first_marker_after(4) == 11
assert DataStreamBuffer("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw").first_marker_after(14) == 26

with open("input.txt", encoding="utf-8") as file:
    buffer = file.readline()
ds = DataStreamBuffer(buffer)

print(f"Datastream buffer needed {ds.first_marker_after(4)} characters to be "
      f"processed before the first start-of-packet marker was detected (4 chars buffer)")
print(f"Datastream buffer needed {ds.first_marker_after(14)} characters to be "
      f"processed before the first start-of-packet marker was detected (14 chars buffer)")
