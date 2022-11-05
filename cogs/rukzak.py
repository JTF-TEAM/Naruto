import nextcord
from nextcord.ext import commands
import random
import motor.motor_asyncio as mator

MONGO = 'mongodb+srv://ASD123:ASD123@cluster0.nfyepgf.mongodb.net/?retryWrites=true&w=majority'

connection = mator.AsyncIOMotorClient(MONGO)
mogo = connection['JTF']
cursorik = mogo.rukzan

class rukzak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = [1038523848880042036,1038523850373210203,1038523853208563852,1038523855196668054]
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == '-init me':
            await cursorik.insert_one(
                {
                    'member_id': message.author.id,
                    'roles':self.roles
                }
            )
            await message.add_reaction('🤡')
        pass
    

    @nextcord.slash_command(name='rukzan')
    async def rukzan(self, interaction):
        rukzan = await cursorik.find_one({'member_id':interaction.user.id})
        if rukzan != None:
            vadim = ''

            for role_id in rukzan['roles']:
                crole = interaction.guild.get_role(role_id)
                if crole != None:
                    vadim += f"{crole.mention}\nID[{crole.id}]"
                    if crole in interaction.user.roles:
                        vadim += '😁\n'
                    else:
                        vadim += '☹\n'

            E = nextcord.Embed(
                title='ur roles',
                description=vadim
            )
            await interaction.response.send_message(embed=E)
        else:
            await interaction.response.send_message('net')
    

    @nextcord.slash_command(name='rukzan_nadet')
    async def asdawdqe(self, interaction, role_id:str):
        rukzan = await cursorik.find_one({'member_id':interaction.user.id})
        if rukzan != None:
            wanted_role = interaction.guild.get_role(int(role_id))
            if wanted_role != None:
                if wanted_role.id in rukzan['roles']:
                    await interaction.user.add_roles(wanted_role)
                    await interaction.response.send_message('gatova')
                else:
                    await interaction.response.send_message('net')
            else:
                await interaction.response.send_message('netu takoi role')
        pass



    @nextcord.slash_command(name='rukzan_snat')
    async def asdaqwewdqe(self, interaction, role_id:str):
        rukzan = await cursorik.find_one({'member_id':interaction.user.id})
        if rukzan != None:
            wanted_role = interaction.guild.get_role(int(role_id))
            if wanted_role != None:
                if wanted_role.id in rukzan['roles']:
                    await interaction.user.remove_roles(wanted_role)
                    await interaction.response.send_message('gatova')
                else:
                    await interaction.response.send_message('net')
            else:
                await interaction.response.send_message('netu takoi role')
        pass

def setup(bot):
    bot.add_cog(rukzak(bot))