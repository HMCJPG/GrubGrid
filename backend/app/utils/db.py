from typing import Dict
from ..models.user import User
from ..models.post import Post
from ..models.comment import Comment

class InMemoryDB:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.posts: Dict[int, Post] = {}
        self.comments: Dict[int, Comment] = {}
        self.user_counter = 1
        self.post_counter = 1
        self.comment_counter = 1

    def add_user(self, user: User) -> User:
        user.id = self.user_counter
        self.users[self.user_counter] = user
        self.user_counter += 1
        return user

    def add_post(self, post: Post) -> Post:
        post.id = self.post_counter
        self.posts[self.post_counter] = post
        self.post_counter += 1
        return post

    def add_comment(self, comment: Comment) -> Comment:
        comment.id = self.comment_counter
        self.comments[self.comment_counter] = comment
        self.comment_counter += 1
        return comment

db = InMemoryDB()
