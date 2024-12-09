from discord.ui import Modal, TextInput
from discord import Interaction, TextStyle
from core.tools import send_bot_embed
from controllers import add_item_code


class AddCodes(Modal, title="Add Codes"):
    def __init__(self, item_id: int, **kwargs):
        super().__init__(**kwargs)
        self.item_id = item_id

        self.codes = TextInput(
            label="Enter the codes you would like to add.",
            style=TextStyle.long,
            placeholder="Enter the codes here, seperate them with a space.",
            required=True,
            max_length=400,
        )
        self.add_item(self.codes)

    async def on_submit(self, interaction: Interaction) -> None:
        try:
            codes = self.codes.value.split()
            await add_item_code(self.item_id, codes)
            await send_bot_embed(
                interaction,
                description="✅ The codes have been added successfully.",
                ephemeral=True,
            )
        except Exception as e:
            print(e)
            await send_bot_embed(
                interaction, description=f"❌ An error occurred.", ephemeral=True
            )
