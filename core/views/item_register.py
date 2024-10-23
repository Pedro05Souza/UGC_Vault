from discord.ui import View, Button
from discord import Member

class ItemRegisterView(View):
    
        def __init__(self, item, author: Member):
            super().__init__(timeout=None)
            self.item = item
            self.author = author
    
        async def interaction_check(self, interaction):
            return interaction.user.id == self.author.id
