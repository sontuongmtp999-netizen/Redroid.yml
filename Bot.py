import discord
from discord import app_commands
import os
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
        # Dùng bcsfe để tải save trực tiếp từ hệ thống Transfer Code của The Battle Cats
        save_file = bcsfe.core.Save.from_transfer_code(transfer_code, confirmation_code)
        
        if not save_file:
            await interaction.followup.send("Không thể tải save! Kiểm tra lại Transfer Code hoặc Confirmation Code xem đúng chưa.")
            return

        # Tiến hành bơm Catfood
        save_file.set_cat_food(amount)
        
        # Xuất ra file save mới để member tải về chép đè
        output_filename = "SAVE_DATA"
        new_save_bytes = save_file.to_bytes()
        
        with open(output_filename, "wb") as f:
            f.write(new_save_bytes)
            
        await interaction.followup.send(
            content=f"Hack thành công **{amount} Catfood** cho tài khoản dùng mã `{transfer_code}`! Tải file `SAVE_DATA` bên dưới về chép vào game:",
            file=discord.File(output_filename)
        )
        os.remove(output_filename)
        
    except Exception as e:
        await interaction.followup.send(f"Có lỗi xảy ra khi kết nối server game hoặc mã sai: `{str(e)}`")

client.run(os.getenv("DISCORD_TOKEN"))
