"""
-*- coding: utf-8 -*-
Async Wrapper for the OpenTDBAPI
"""

from random import choice
from typing import List

from aiotrivia.exceptions import *
from aiotrivia.http import HTTPClient
from aiotrivia.question import Question, CATEGORIES


class TriviaClient:
    """
    The main trivia client used to get questions from the API
    """
    url = 'https://opentdb.com/api.php'
    http = HTTPClient()

    def __repr__(self):
        return f"aiotrivia.client.TriviaClient"

    async def get_random_question(self, difficulty=choice(['easy', 'medium', 'hard'])) -> Question:
        difficulties = ('easy', 'medium', 'hard')
        if difficulty not in difficulties:
            raise InvalidDifficulty("%s is not a valid difficulty!" % difficulty)
        data = await self.http.get(self.url, params={"amount": 1, "difficulty": difficulty})
        return Question(data=data.get('results')[0])

    async def get_specific_question(self, **kwargs) -> List[Question]:
        valid_kwargs = ['amount', 'type', 'category', 'difficulty']
        params = {}
        questions = []
        if any(item not in valid_kwargs for item in kwargs.keys()):
            raise InvalidKwarg(
                "You have passed an invalid keyword argument! Valid keyword arguments include: %s" % ', '.join(
                    valid_kwargs))
        amount, type, category, difficulty = kwargs.get('amount', 1), kwargs.get('type'), kwargs.get(
            'category'), kwargs.get('difficulty')
        if amount:
            if not isinstance(amount, int) or not 0 < amount < 50:
                raise InvalidAmount()
            else:
                params['amount'] = amount
        if type:
            if type.lower() not in ['multiple', 'boolean']:
                raise InvalidType()
            else:
                params['type'] = type
        if category:
            if not isinstance(category, int) or category not in CATEGORIES:
                raise InvalidCategory()
            else:
                params['category'] = category
        if difficulty:
            if difficulty.lower() not in ['easy', 'medium', 'hard']:
                raise InvalidDifficulty()
            else:
                params['difficulty'] = difficulty
        data = await self.http.get(self.url, params)
        for item in data.get('results'):
            questions.append(Question(data=item))
        return questions

    async def close(self):
        await self.http.close()
