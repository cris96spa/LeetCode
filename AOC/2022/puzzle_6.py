"""
--- Day 6: Tuning Trouble ---
The preparations are finally complete; you and the Elves leave camp on foot and begin to make your way toward the star fruit grove.

As you move through the dense undergrowth, one of the Elves gives you a handheld device. He says that it has many fancy features, but the most important one to set up right now is the communication system.

However, because he's heard you have significant experience dealing with signal-based systems, he convinced the other Elves that it would be okay to give you their one malfunctioning device - surely you'll have no problem fixing it.

As if inspired by comedic timing, the device emits a few colorful sparks.

To be able to communicate with the Elves, the device needs to lock on to their signal. The signal is a series of seemingly-random characters that the device receives one at a time.

To fix the communication system, you need to add a subroutine to the device that detects a start-of-packet marker in the datastream. In the protocol being used by the Elves, the start of a packet is indicated by a sequence of four characters that are all different.

The device will send your subroutine a datastream buffer (your puzzle input); your subroutine needs to identify the first position where the four most recently received characters were all different. Specifically, it needs to report the number of characters from the beginning of the buffer to the end of the first such four-character marker.

For example, suppose you receive the following datastream buffer:

mjqjpqmgbljsphdztnvjfqwrcgsmlb
After the first three characters (mjq) have been received, there haven't been enough characters received yet to find the marker. The first time a marker could occur is after the fourth character is received, making the most recent four characters mjqj. Because j is repeated, this isn't a marker.

The first time a marker appears is after the seventh character arrives. Once it does, the last four characters received are jpqm, which are all different. In this case, your subroutine should report the value 7, because the first start-of-packet marker is complete after 7 characters have been processed.

Here are a few more examples:

bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11
How many characters need to be processed before the first start-of-packet marker is detected?
"""

def find_start_of_packet_marker(datastream: str) -> int:
    # Use a set to keep track of unique elements in the window
    for i in range(len(datastream) - 3):
        window = datastream[i:i+4]
        if len(set(window)) == 4:  # Check if all characters in the window are unique
            return i + 4
    return -1

"""
    The provided solution works pretty well under the assumption that the the size
    of the moving windows << the number of elements of the input.
    In our case the time complexity is O(n*4), since at each iteration we are adding all 4 elements to the set, which costs O(4).
    If we consider an arbitrary size window k, the provided solution becomes suboptimal with a time complexity of O(n*k).
    To provide also a general case optimal solution, that computes the marker index in O(n) time, we can rely on a dictionary
    that counts the number of occurrence of each char.
"""
def find_start_of_packet_marker_general(datastream:str, k:int=4) -> int:
   # use a dictionary to keep tracks of seen elements
   chars = {}
   
   # count unique values
   unique_count = 0

   # Perform the initialization with the first k elements
   for i in range(k):
       value = chars.get(datastream[i], 0)
       chars[datastream[i]] = value + 1
       if not value:
           # If counter for current char was 0, increase the unique counter
           unique_count+=1
   
   # If already found, return the first marker index
   if unique_count == k:
       return k
   
   # Iterate over remaining elements with a O(n) time complexity
   for i in range(len(datastream)-k-1):
       # Decrement the counter for the first element
       chars[datastream[i]] -= 1

       # If the counter reaches 0, remove the element from the dict
       if not chars.get(datastream[i], 0):
           del chars[datastream[i]]
           unique_count -= 1
       
       # Consider the last element of the window
       value = chars.get(datastream[i+k], 0)
       chars[datastream[i+k]] = value + 1
       # If not present add to the dict
       if not value:
           unique_count+=1
       
       if unique_count == k:
           return i+k+1
   return -1

