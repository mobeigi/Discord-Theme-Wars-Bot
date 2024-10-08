import traceback
import discord
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
import textwrap
import tempfile

""" Cog that generates secret light/dark messages """

class ThemeWars(commands.Cog):
    """ThemeWars"""

    def __init__(self, bot):
        self.bot = bot
        self.font = ImageFont.truetype("../assets/interlaced-font.ttf", 42)
        self.image_width_max = 400
        self.image_height_max = 250
        self.line_max_char_width = 16

    @commands.command(name='themewars', aliases=['tw'], brief='Generate Light/Dark Message', 
        description='Generates a special message that shows differently based on users light/dark theme preference')
    async def themewars(self, ctx, light_theme_message : str,  dark_theme_message : str):
        try:
            # Delete original message
            await ctx.message.delete()

            # Create image
            temp_file = await self._create_image(light_theme_message, dark_theme_message)

            # Send Image
            await ctx.send(file=discord.File(open(temp_file.name, "rb")))
        except Exception as e:
            print("An error occurred:", e)
            traceback.print_exc()
            await ctx.send("`An error occurred while processing your request.`")

    async def _create_image(self, light_theme_message, dark_theme_message):
        img = Image.new("RGBA", (self.image_width_max, self.image_height_max), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Disable anti-alaising, we need sharp edges
        draw.fontmode = '1'

        # Draw light component (what light users see, dark text)
        width_offset = max_light_width = 4
        height_offset = total_light_height = 4

        for line in textwrap.wrap(light_theme_message, width=self.line_max_char_width):
            draw.text((width_offset, height_offset), line, font=self.font, fill="#36393f")
            height_offset += self._get_size(self.font, line)[1] * 1.2
            total_light_height += self._get_size(self.font, line)[1] * 1.2
            max_light_width = max(max_light_width, self._get_size(self.font, line)[0])

        # Draw dark component (what dark users see, light text)
        width_offset = max_dark_width = 4
        height_offset = total_dark_height = 6
        for line in textwrap.wrap(dark_theme_message, width=self.line_max_char_width):
            draw.text((width_offset, height_offset), line, font=self.font, fill="#ffffff")
            height_offset += self._get_size(self.font, line)[1] * 1.2
            total_dark_height += self._get_size(self.font, line)[1] * 1.2
            max_dark_width = max(max_dark_width, self._get_size(self.font, line)[0])

        # Crop image to maximum width, height boundaries
        # Maximum image dimensions has to be fairly small, otherwise Discord seems to compress image/mess with pixels
        # Which makes the interlace effect not work correctly.
        max_width = max(max_dark_width, max_light_width)
        max_height = max(total_dark_height, total_light_height)
        img = ImageOps.crop(img, (0, 0, max(0, self.image_width_max - max_width), max(0, self.image_height_max - max_height)))
        
        # Save to temp file and return path
        temp_file = tempfile.NamedTemporaryFile(suffix='.png')

        img.save(fp = temp_file.name, format='PNG', quality=100, optimize=True, progressive=True)
        return temp_file

    def _get_size(self, font, s):
        left, top, right, bottom = font.getbbox(s)
        width, height = right - left, bottom - top
        size = width, height
        return size

    @themewars.error
    async def local_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("`You did not provide the '" + error.param.name + "' parameter.`")

async def setup(bot):
    await bot.add_cog(ThemeWars(bot))
