import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. --- WEBSITE FOR 24/7 KEEP ALIVE ---
app = Flask('')

@app.route('/')
def home():
    return "Ashmi Plays Bot is Alive 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# 2. --- DISCORD BOT SETUP ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 3. --- VERIFICATION BUTTON SYSTEM WITH YOUR REAL LINKS ---
class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify Here ✅", style=discord.ButtonStyle.green, custom_id="verify_btn")
    async def verify_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Member")
        
        if role:
            if role in interaction.user.roles:
                await interaction.response.send_message("❌ Aap pehle se hi verify ho chuke hain!", ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("🎉 ✅ Successfully verify ho gaye hain!", ephemeral=True)
                
                # --- VIP EMBED MESSAGE WITH YT & SMP PROMOTION ---
                try:
                    embed_dm = discord.Embed(
                        title="🛡️ Verification Successful!",
                        description=f"👋 Hey {interaction.user.mention},\nAap **{interaction.guild.name}** server mein successfully verify ho gaye hain! 🎉\nAapko **Member** role de diya gaya hai.",
                        color=discord.Color.green()
                    )
                    
                    # YouTube Channel Promotion (Links Updated!)
                    embed_dm.add_field(
                        name="📺 Mera YouTube Channel!",
                        value="Bhai ka channel hai, **Subscribe karna mat bhoolna!** Support dikhao full:\n🔗 [Yahan Click Karke Subscribe Karein!](https://www.youtube.com/@Ashmiplays91)",
                        inline=False
                    )
                    
                    # ReaperCraft SMP Information
                    embed_dm.add_field(
                        name="🎮 Join Our ReaperCraft SMP!",
                        value="Hamari khud ki ekdam mazedar Minecraft SMP hai jisme aap khel kar mazedar **Crates** open kar sakte hain! Aap isme **Free** mein bhi khel sakte hain aur maze le sakte hain. Agar aapko extra maze chahiye toh aap **Ranks** bhi buy kar sakte hain!",
                        inline=False
                    )
                    
                    # Cheap Premium Servers Info (Links Updated!)
                    embed_dm.add_field(
                        name="🛒 Cheap Premium Servers & Info:",
                        value="* 🌐 **Website:** [reapercraft.online](http://reapercraft.online/) (Yahan click karke apna khud ka server banayein)\n* 💰 Rates dekhne ke liye **#reapercraft** section check karein.\n* 🧪 Aap chahein toh server ka **Free Trial** bhi le sakte hain!\n* 🎫 Kisi bhi help ya support ke liye server mein **Ticket** banayein.",
                        inline=False
                    )
                    
                    embed_dm.set_footer(text=f"Rules follow karein aur enjoy karein! | {interaction.guild.name} & ReaperCraft")
                    
                    # User ke DM mein bhej rahe hain
                    await interaction.user.send(embed=embed_dm)
                    
                except discord.Forbidden:
                    print(f"⚠️ {interaction.user.name} ka DM band hai, isliye promo DM nahi gaya.")
        else:
            await interaction.response.send_message("❌ Server mein 'Member' role nahi mila! Server settings mein jaakar 'Member' naam ka role banayein.", ephemeral=True)

# 4. --- BOT ONLINE EVENT ---
@bot.event
async def on_ready():
    bot.add_view(VerifyButton())
    print(f'==========================================')
    print(f'🎉 {bot.user.name} ALL-IN-ONE PROMO BOT ONLINE!')
    print(f'==========================================')
    await bot.change_presence(activity=discord.Game(name="Prefix is ! | !setup_verify ⚙️"))

# 5. --- COMMAND TO SETUP BUTTON (ADMIN ONLY) ---
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_verify(ctx):
    embed = discord.Embed(
        title="🔒 Server Verification",
        description="Server ke baaki channels dekhne aur access pane ke liye neeche diye gaye **Verify Here ✅** button par click karein!",
        color=discord.Color.green()
    )
    embed.set_footer(text="Ashmi Plays Security System")
    
    await ctx.send(embed=embed, view=VerifyButton())
    await ctx.message.delete()

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN')
