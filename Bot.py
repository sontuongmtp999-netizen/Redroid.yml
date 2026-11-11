import os
import discord
from discord import app_commands
import bcsfe

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
@app_commands.describe(
    transfer_code="Mã chuyển dữ liệu lấy trong game", 
    confirmation_code="Mã xác nhận", 
    amount="Số lượng Catfood muốn hack"
)
async def hack_catfood(interaction: discord.Interaction, transfer_code: str, confirmation_code: str, amount: int):
    await interaction.response.defer(thinking=True)
    
    try:
        if amount <= 0 or amount > 999999:
            await interaction.followup.send("Số lượng Catfood không hợp lệ! Vui lòng nhập từ 1 đến 999,999.")
            return

        # Khởi tạo thông tin server request từ bcsfe
        # bcsfe hỗ trợ tải dữ liệu thông qua lớp tương tác server chính hãng
        country = bcsfe.core.CountryCode.EN  # Mặc định tiếng Anh, đổi sang JP/TW/KR nếu cần
        
        # Gọi hàm lấy save từ transfer code đúng chuẩn cấu trúc module hiện tại của bcsfe
        save_file = bcsfe.core.ServerData.get_save_data(
            transfer_code.strip(), 
            confirmation_code.strip(), 
            country
        )
        
        if not save_file:
            await interaction.followup.send("Không thể tải save! Kiểm tra lại Transfer Code, Confirmation Code hoặc chọn đúng phiên bản server.")
            return

        # Sửa số lượng catfood
        save_file.set_cat_food(amount)
        
        # Xuất file save chuẩn
        output_filename = "SAVE_DATA"
        save_file.write(output_filename)
            
        await interaction.followup.send(
            content=f"Đã hack thành công **{amount:,} Catfood** cho mã `{transfer_code}`! Tải file `SAVE_DATA` dưới đây về chép đè vào game:",
            file=discord.File(output_filename)
        )
        
        if os.path.exists(output_filename):
            os.remove(output_filename)
            
    except Exception as e:
        await interaction.followup.send(f"Lỗi kết nối server Ponos hoặc sai mã: `{str(e)}`")

client.run(TOKEN)
