import os
import discord
from discord import app_commands
import bcsfe

class BattleCatsBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Bot đã online với tên: {self.user}")

client = BattleCatsBot()

@client.tree.command(name="hack_catfood", description="Nhập Transfer Code để bơm Catfood tự động!")
@app_commands.describe(transfer_code="Mã chuyển dữ liệu trong game", confirmation_code="Mã xác nhận", amount="Số lượng Catfood muốn hack")
async def hack_catfood(interaction: discord.Interaction, transfer_code: str, confirmation_code: str, amount: int):
    await interaction.response.defer(thinking=True)
    
    try:
        # Tải save trực tiếp từ hệ thống Transfer Code của The Battle Cats
        save_file = bcsfe.core.Save.from_transfer_code(transfer_code, confirmation_code)
        
        if not save_file:
            await interaction.followup.send("Không thể tải save! Kiểm tra lại Transfer Code hoặc Confirmation Code.")
            return

        # Bơm Catfood
        save_file.set_cat_food(amount)
        
        output_filename = "SAVE_DATA"
        new_save_bytes = save_file.to_bytes()
        
        with open(output_filename, "wb") as f:
            f.write(new_save_bytes)
            
        await interaction.followup.send(
            content=f"Hack thành công **{amount} Catfood** cho tài khoản `{transfer_code}`! Tải file `SAVE_DATA` dưới đây về chép vào game:",
            file=discord.File(output_filename)
        )
        os.remove(output_filename)
        
    except Exception as e:
        await interaction.followup.send(f"Có lỗi xảy ra hoặc mã sai: `{str(e)}`")

# Nhét trực tiếp token vào đây, khỏi cần biến môi trường lằng nhằng
client.run("MTU2NDQwNjk3NjM4Mzk0NjgwMg.GH-NpE.rQ5jRukTE6iIGRfp8-EO4tGiqS9Q8vuI-wUmIY")
