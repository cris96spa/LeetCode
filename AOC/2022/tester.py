
from puzzle_6 import find_start_of_packet_marker

def test_find_start_of_packet_marker():
    assert find_start_of_packet_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert find_start_of_packet_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert find_start_of_packet_marker("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert find_start_of_packet_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert find_start_of_packet_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

if __name__ == "__main__":
    test_find_start_of_packet_marker()