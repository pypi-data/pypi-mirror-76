"""
-*- coding: utf-8 -*-
The files containing question data
"""

from html import unescape
from random import randint

CATEGORIES = {
    9: "General Knowledge",
    10: "Entertainment: Books",
    11: "Entertainment: Film",
    12: "Entertainment: Music",
    13: "Entertainment: Musicals & Theatres",
    14: "Entertainment: Television",
    15: "Entertainment: Video Games",
    16: "Entertainment: Board Games",
    17: "Science & Nature",
    18: "Science: Computers",
    19: "Science: Mathematics",
    20: "Mythology",
    21: "Sports",
    22: "Geography",
    23: "History",
    24: "Politics",
    25: "Art",
    26: "Celebrities",
    27: "Animals",
    28: "Vehicles",
    29: "Entertainment: Comics",
    30: "Science: Gadgets",
    31: "Entertainment: Japanese Anime & Manga",
    32: "Entertainment: Cartoon & Animations"
}



class Question:
    """
    The question type returned when getting questions
    """
    __slots__ = ('category', 'type', 'question', 'answer', 'custom_incorrect', 'incorrect_answers', 'difficulty', 'num')

    def __init__(self, data: dict):
        self.category = data.get('category')
        self.type = data.get('type')
        self.question = unescape(str(data.get('question')))
        self.answer = unescape(str(data.get('correct_answer')))
        self.custom_incorrect = []
        self.incorrect_answers: list = [unescape(answer) for answer in data.get('incorrect_answers')]
        self.difficulty = data.get('difficulty')
        self.num = 0

    def __repr__(self):
        return f"<aiotrivia.question.Question: question={self.question}, category={self.category}, type={self.type}>"

    def add_incorrect_answers(self, *args):
        for item in args:
            self.custom_incorrect.append(item)

    @property
    def incorrect_responses(self):
        return self.custom_incorrect + self.incorrect_answers

    @property
    def responses(self):
        if not self.num:
            self.num = randint(1, len(self.incorrect_responses))
        return self.incorrect_responses[:self.num-1] + [self.answer] + self.incorrect_responses[self.num-1:]
