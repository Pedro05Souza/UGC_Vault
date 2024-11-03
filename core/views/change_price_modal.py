from discord.ui import Modal, TextInput
from discord import Interaction, TextStyle
from core.tools import send_bot_embed
from controllers import update_item_price

class ChangePrice(Modal, title="Change Item Price"):
    def __init__(self, item_id: int, **kwargs):
        super().__init__(**kwargs)
        self.item_id = item_id

        self.updated_price = TextInput (
            label="Enter the price you would like to set.",
            style=TextStyle.short,
            placeholder="Enter the price here.",
            required=True,
            max_length=100
        )
        self.add_item(self.updated_price)

    async def on_submit(self, interaction: Interaction) -> None:
        try:
            updated_price = int(self.updated_price.value)
            await update_item_price(self.item_id, updated_price)
            await send_bot_embed(interaction, description="✅ The price has been updated sucessfully.", ephemeral=True)
        except Exception as e:
            print(e)
            await send_bot_embed(interaction, description=f"❌ An error occurred.", ephemeral=True)

