from discord.ui import View, Select
from discord import Interaction, SelectOption, Member
from controllers import get_user_balance, update_user, get_code_from_item
from core.tools import send_bot_embed, confirmation_popup, embed_builder
from tortoise.transactions import in_transaction

class ItemList(View):
    
    def __init__(self, buyer: Member, items: list, has_more: bool) -> None:
        super().__init__(timeout=None)
        
        self.items = items
        self.buyer = buyer
        self.has_more = has_more
        select = self.add_select()
        
        select.callback = self.callback
        
        self.add_item(select)
        
    def add_options(self) -> list[SelectOption]:
        return [
            SelectOption(
                label=item["item_name"],
                value=item["item_id"],
                description=f"{item['item_price']} candies",
            ) for item in self.items
        ]
    
        
    def add_select(self) -> None:
        return (
            Select(
                placeholder="Select the items you want to purchase",
                options=self.add_options(),
                custom_id="purchase_items",
                min_values=1,
                max_values=len(self.items),
            )
        )
        
    async def callback(self, interaction: Interaction) -> None:
        """
        callback function for the select menu

        Args:
            interaction (Interaction): The interaction object
        """
        if interaction.user.id != self.buyer.id:
            return await send_bot_embed(interaction, description="❌ You are not allowed to interact with this select menu.", ephemeral=True)
        
        chosen_items = [item for item in self.items if str(item["item_id"]) in interaction.data["values"]]
        
        total_price = sum([item["item_price"] for item in chosen_items])
        user_balance = await get_user_balance(self.buyer.id)
    
        
        if total_price > user_balance:
            return await send_bot_embed(interaction, description="❌ You do not have enough balance to purchase these items.", ephemeral=True)
    
        formatted_items = "\n".join([f"**{item['item_name']}** - {item['item_price']} candies" for item in chosen_items])
        
        embed = await embed_builder(
            title="Confirm Purchase",
            description=f"Are you sure you want to purchase the following items for {total_price} candies?\n\n{formatted_items}",
        )
        
        if not await confirmation_popup(interaction, embed):
            return
        
        await self.dispatch_item_codes(interaction, chosen_items, total_price, user_balance)
    
    async def dispatch_item_codes(self, interaction: Interaction, chosen_items: list, total_price: int, previous_balance: int) -> None:
        """
        Dispatch the item codes to the user who purchased the items

        Args:
            chosen_items (list): The items that the user has chosen to purchase
        """
        async with in_transaction():
            failure_error_message = "❌ Oops! Something went wrong and i couldn't send you the codes. Don't worry, your money has been refunded and you can buy the items again."
            await update_user(self.buyer.id, balance=previous_balance - total_price)
            
            all_codes = []
            
            for item in chosen_items:
                codes = await get_code_from_item(item["item_id"])
                all_codes.append(codes)
                
            if any([not codes for codes in all_codes]):
                failure_error_message = "❌ Oops! Someone else bought the items before you did. Don't worry, your money has been refunded and you can buy the items again."
                
                return await send_bot_embed(
                    interaction,
                    description=failure_error_message,
                    ephemeral=True,
                )
                
            await send_bot_embed(
                interaction,
                description=f"✅ You have successfully purchased the following items:\n\n".join([f"Item: **{item['item_name']}**\nCode: {code}" for item, code in zip(chosen_items, all_codes)]),
                is_dm=True,
                dm_failure_error_message=failure_error_message,
            )
            
            
        