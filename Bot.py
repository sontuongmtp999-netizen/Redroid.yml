import os
import discord
from discord import app_commands
import bcsfe

# Đọc token an toàn từ hệ thống GitHub Actions Secret
TOKEN = os.getenv("DISCORD_TOKEN")

class BattleCatsBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Bot đã online với tên: {self.user}")

client = BattleCatsBot()

@client.tree.command(name="hack_catfood", description="Nhập Transfer Code để bơm Catfood tự động!")
@app_commands.describe(transfer_code="Mã chuyển dữ liệu", confirmation_code="Mã xác nhận", amount="Số lượng Catfood")
async def hack_catfood(interaction: discord.Interaction, transfer_code: str, confirmation_code: str, amount: int):
    await interaction.response.defer(thinking=True)
    try:
        save_file = bcsfe.core.Save.from_transfer_code(transfer_code, confirmation_code)
        if not save_file:
            await interaction.followup.send("Sai mã chuyển dữ liệu hoặc mã xác nhận!")
            return
        save_file.set_cat_food(amount)
        output_filename = "SAVE_DATA"
        with open(output_filename, "wb") as f:
            f.write(save_file.to_bytes())
        await interaction.followup.send(content=f"Hack thành công **{amount} Catfood**!", file=discord.File(output_filename))
        os.remove(output_filename)
    except Exception as e:
        await interaction.followup.send(f"Lỗi: `{str(e)}`")

client.run(TOKEN)
