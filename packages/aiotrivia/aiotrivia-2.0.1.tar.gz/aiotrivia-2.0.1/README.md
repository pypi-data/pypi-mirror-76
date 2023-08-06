# aiotrivia
Async Wrapper for the OpenTDB API

### Installation
```sh
$ pip install git+https://github.com/niztg/aiotrivia
```

### Example Usage
```py
import asyncio
import aiotrivia

client = aiotrivia.TriviaClient()

async def main():
    data = await client.get_specific_question(category=20)
    for i in data:
        print('%s | %s' % (i.question, i.responses))
    await client.close() # after you're done with everything

asyncio.get_event_loop().run_until_complete(main())
```

#### Returns:
`Which figure from Greek mythology traveled to the underworld to return his wife Eurydice to the land of the living? | ['Daedalus', 'Hercules', 'Perseus', 'Orpheus']`

### discord.py command usage

```py
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands
import asyncio
import random

class TriviaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia = TriviaClient()
        
    @commands.command()
    async def trivia(self, ctx, difficulty):
        try:
            question = await self.trivia.get_random_question(difficulty)
        except AiotriviaException as error:
            return await ctx.send(f"{error.__class__.__name__}: {error}")
        answers = question.responses
        random.shuffle(answers)
        final_answers = '\n'.join([f"{index}. {value}" for index, value in enumerate(answers, 1)])
        message = await ctx.send(f"**{question.question}**\n{final_answers}\n{question.type.capitalize()} Question about {question.category}")
        answer = answers.index(question.answer)+1
        await self.trivia.close() # cleaning up
        try:
            while True:
                msg = await self.client.wait_for('message', timeout=15, check=lambda m: m.id != message.id)
                if str(answer) in msg.content:
                    return await ctx.send(f"{answer} was correct! ({question.answer})")
        except asyncio.TimeoutError:
            await ctx.send(f"The correct answer was {question.answer}")

def setup(bot):
    bot.add_cog(TriviaCog(bot))
```
#### <a href=https://github.com/niztg/aiotrivia/wiki>For more info, read the documentation</a>
#### <a href=https://cybertron-5k.netlify.app/server>Or join the discord server</a>
