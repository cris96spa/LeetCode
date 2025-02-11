from heapq import heappush, heappop
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self):
        self.timestamp = 0  # Global counter to maintain tweet order
        self.tweets = defaultdict(list)  # Maps userId -> list of (timestamp, tweetId)
        self.following = defaultdict(set)  # Maps userId -> set of users they follow

    def postTweet(self, userId: int, tweetId: int) -> None:
        """Compose a new tweet."""
        self.tweets[userId].append((self.timestamp, tweetId))
        self.timestamp += 1  # Increment timestamp for ordering

    def getNewsFeed(self, userId: int) -> List[int]:
        """Retrieve the 10 most recent tweets from user and followees."""
        min_heap = []

        # Users to fetch tweets from (including self)
        users = self.following[userId] | {userId}

        for user in users:
            if self.tweets[user]:  # If the user has tweets
                for tweet in self.tweets[user][
                    -10:
                ]:  # Get the last 10 tweets (most recent)
                    heappush(min_heap, tweet)
                    if len(min_heap) > 10:  # Maintain at most 10 elements
                        heappop(min_heap)

        # Sort tweets from most recent to least recent
        return [tweetId for _, tweetId in sorted(min_heap, reverse=True)]

    def follow(self, followerId: int, followeeId: int) -> None:
        """FollowerId follows followeeId."""
        if followerId != followeeId:  # Users cannot follow themselves
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """FollowerId unfollows followeeId."""
        self.following[followerId].discard(followeeId)  # Remove safely
