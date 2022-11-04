import nextcord
from nextcord.ext import commands
import random
import motor.motor_asyncio as mator
from dotenv import mongo as MONGO

connection = mator.AsyncIOMotorClient(MONGO)
mogo = connection['JTF']

class CCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name='clan_list', description='кланы серверба')
    async def ldfjkadjflkjadf(self, interaction: nextcord.Interaction):
        claninfo = mogo.clans.find({})
        E = nextcord.Embed(title='Активные кланы')
        total_negrov = 0
        async for clan in claninfo:
            E.add_field(
                name=clan['clan_name'],
                value='ID: ' + str(clan['clan_id']),
                inline=False
            )

            total_negrov += 1
        if total_negrov != 0:
            await interaction.response.send_message(embed=E)
        else:
            await interaction.response.send_message("На сервере ноль кланов")

    
    @nextcord.slash_command(name='clan_my', description='инфо о вашем клане')
    async def chela_clan(self, interaction: nextcord.Interaction):
        claninfo = await mogo.clans.find_one({'owner_id': interaction.user.id})
        if claninfo != None:

            try:
                e = nextcord.Embed(
                title=claninfo['clan_name'],
                description=claninfo['clan_bio'] + '\nID: ' + str(claninfo['clan_id']) + f"\nЧЕЛОВ всего: {len(claninfo['member'])}"
            )
                e.set_image(url=claninfo['clan_icon'])
                await interaction.response.send_message(embed=e)
            except:
                e = nextcord.Embed(
                title=claninfo['clan_name'],
                description=claninfo['clan_bio'] + '\nID: ' + str(claninfo['clan_id']) + f"\nЧЕЛОВ всего: {len(claninfo['member'])}"
            )
                e.set_image(url='https://myakamai.force.com/customers/servlet/rtaImage?eid=ka34R000000c8CJ&feoid=00N0f00000FlxAK&refid=0EM4R000001zhdU')
                await interaction.response.send_message(embed=e)
        else:
            await interaction.response.send_message('у вас нету клана')
        
    
    @nextcord.slash_command(name='clan_create', description='создание клана на сервербе')
    async def create_clan(self, interaction: nextcord.Interaction, clan_name: str, description: str = '/clan_set_bio для установки описания', pic_url:str='https://www.pngitem.com/pimgs/m/254-2549834_404-page-not-found-404-not-found-png.png'):
        if await mogo.clans.find_one({'owner_id': interaction.user.id}) != None:
            await interaction.response.send_message(' по одному клану на рыло')
        else:
            clan_id = random.randint(1000000,99999999)
            clanboss_data = await mogo.infousers.find_one({'member_id':interaction.user.id})
            print(clanboss_data)
            if clanboss_data != None:
                if clanboss_data['money'] > 10000:
                    clan_role = await interaction.guild.create_role(name=clan_name)
                    category = interaction.guild.get_channel(1023748851976380557)
                    clan_text = await category.create_text_channel(name=clan_name)
                    clan_voice = await category.create_voice_channel(name=clan_name)
                    await mogo.clans.insert_one( {
                            'guild_id': interaction.guild.id,
                            'owner_id': interaction.user.id,
                            'clan_id': clan_id,
                            'member': [interaction.user.id],
                            'cash_clan':0,
                            'clan_icon': pic_url,
                            'clan_role': clan_role.id,
                            'clan_shop':[],
                            'clan_name':clan_name,
                            'clan_bio': description,
                            'clan_voice_id': clan_voice.id,
                            'clan_text_id': clan_text.id
                            }           
                        )
                    new_money = clanboss_data['money'] - 1
                    await mogo.infousers.update_one(clanboss_data,{'$set':{'money':new_money}})
                    await interaction.response.send_message(f'Клан создан. Клан айди {clan_id}\nС вашего счета списано 10000 шекелей')
                else:
                    await interaction.response.send_message(f'Malo denyak dlya etogo{clan_id}')
            else:
                await interaction.response.send_message(f'Что то пошло не так')


    @nextcord.slash_command(name='clan_delete', description='Удоление клана на сервербе')
    async def delete_clan(self, interaction: nextcord.Interaction, clan_id: int):
        clan = await mogo.clans.find_one({'clan_id':clan_id})
        if clan != None:
            if clan['owner_id'] == interaction.user.id:
                clan_text = interaction.guild.get_channel(clan['clan_voice_id'])
                clan_voice = interaction.guild.get_channel(clan['clan_text_id'])
                clan_role = interaction.guild.get_role(clan['clan_role'])
                await clan_role.delet()
                await clan_text.delete()
                await clan_voice.delete()
                await mogo.clans.delete_one({'clan_id': clan_id})
                await interaction.response.send_message('Клан удолен')
            else:
                await interaction.response.send_message("Это не ваш клан...")
        else:
            await interaction.response.send_message("Клан не найден...")

    class waitforjoin(nextcord.ui.View):
        def __init__(self):
            super().__init__(timeout=60*5)
            self.value = None


        @nextcord.ui.button(label='вступить')
        async def join(self, button: nextcord.ui.Button, interaction):
            self.value = True
            self.stop()
        
        @nextcord.ui.button(label='отказаться')
        async def nenihuja(self, button: nextcord.ui.Button, interaction):
            self.value = False
            self.stop()

    @nextcord.slash_command(name='clan_add_member', description='добавление микрочелика в клан')
    async def add_member(self, interaction: nextcord.Interaction, member: nextcord.Member, clan_id: int):
        all_clans_members = []
        claninfo = mogo.clans.find({})
        async for shit in claninfo:
            all_clans_members += shit['member']
        
        if member.id in all_clans_members:
            await interaction.response.send_message('низя вступать в многокланов')
        else:
            clan = await mogo.clans.find_one({'clan_id':clan_id})
            if clan != None:
                if clan['owner_id'] == interaction.user.id:
                    if member.id in clan['member']:
                        await interaction.response.send_message('чел уже в клане')
                    else:
                        baton = self.waitforjoin()
            
                        msg = await interaction.response.send_message(
                            content=member.mention,
                            embed=nextcord.Embed(
                                title="Приглашение в клан",
                                description = f"{interaction.user.mention} приглашает вас в клан {clan['clan_name']}",
                                color=0xf45ffa
                                ),
                                view=baton
                            )
                        await baton.wait()
                        if baton.value == None:
                            await msg.edit(
                            content=interaction.user.mention,
                            embed=nextcord.Embed(
                                title="Время ожидания ответа вышло",
                                description = f"Пользователь {member.mention} не определился",
                                color=0xf45ffa
                                
                                ),view=None)
                        else:
                            await msg.edit(view=None)
                            if baton.value:
                                new_data = clan.copy()
                                new_data['member'].append(member.id)
                                clan_role = interaction.guild.get_role(clan['clan_role'])
                                await member.add_roles(clan_role)
                                await mogo.clans.update_one({'clan_id':clan_id}, {'$set': new_data})
                                await msg.edit(
                                    content=interaction.user.mention,
                                    embed=nextcord.Embed(
                                        title="Заявка одобрена",
                                        description = f"Пользователь {member.mention} вступает в клан",
                                        color=0xf45ffa
                                
                                ),view=None)
                            else:
                                await msg.edit(
                                    content=interaction.user.mention,
                                    embed=nextcord.Embed(
                                        title="Заявка отклонена",
                                        description = f"Пользователь {member.mention} не принял запрос",
                                        color=0xf45ffa
                                
                                ),view=None)              
                else:
                    await interaction.response.send_message("Это не ваш клан...")
            else:
                await interaction.response.send_message("Что то пошло не так... ")


    @nextcord.slash_command(name='clan_remove_member', description='кик микрочелика')
    async def remove_member(self, interaction: nextcord.Interaction, member: nextcord.Member, clan_id: int):
        clan = await mogo.clans.find_one({'clan_id':clan_id})
        if clan != None:
            if clan['owner_id'] == interaction.user.id:
                if member.id in clan['member']:
                    new_data = clan.copy()
                    new_data['member'].remove(member.id)
                    await mogo.clans.update_one({'clan_id':clan_id}, {'$set': new_data})
                    await interaction.response.send_message(f'Пользователь уадлен')
                else:
                    await interaction.response.send_message(f'Пользователь не состоит в данном клане')
            else:
                await interaction.response.send_message("Это не ваш клан...")
        else:
            await interaction.response.send_message("Что то пошло не так... ")
    

    @nextcord.slash_command(name='clan_set_bio', description='задать описание клана')
    async def set_bio(self, interaction: nextcord.Interaction, new_bio: str, clan_id: int):
        clan = await mogo.clans.find_one({'clan_id':clan_id})
        if clan != None:
            if clan['owner_id'] == interaction.user.id:
                new_data = clan.copy()
                new_data['clan_bio'] = new_bio
                await mogo.clans.update_one({'clan_id':clan_id}, {'$set': new_data})
                await interaction.response.send_message(f'Готово')
            else:
                await interaction.response.send_message("Это не ваш клан...")
        else:
            await interaction.response.send_message("Что то пошло не так... ")
    
    @nextcord.slash_command(name='clan_set_pic', description='сменить картинку клана')
    async def set_pix(self, interaction: nextcord.Interaction, new_pic_url: str, clan_id: int):
        clan = await mogo.clans.find_one({'clan_id':clan_id})
        if clan != None:
            if clan['owner_id'] == interaction.user.id:
                new_data = clan.copy()
                new_data['clan_icon'] = new_pic_url
                await mogo.clans.update_one(clan, {'$set': new_data})
                await interaction.response.send_message(f'Готово')
            else:
                await interaction.response.send_message("Это не ваш клан...")
        else:
            await interaction.response.send_message("Что то пошло не так... ")
    
    @nextcord.slash_command(name='clan_send_money', description='закинуть деняк в клан')
    async def send_money(self, interaction: nextcord.Interaction, how_much: int, clan_id: int):
        if how_much >0:
            user_data = await mogo.infousers.find_one({'member_id': interaction.user.id})
            if user_data['money'] >= how_much:
                clan = await mogo.clans.find_one({'clan_id':clan_id})
                if clan != None:
                    new_data = clan.copy()
                    new_data['cash_clan'] += how_much
                    await mogo.clans.update_one(clan, {'$set': new_data})
                    await interaction.response.send_message(f'Готово')
                else:
                    await interaction.response.send_message("Не получилось найти клан... ")
            else:
                await interaction.response.send_message(" Мало денег...")
        else:
            await interaction.response.send_message('ахахаха, чел....')
        
    @nextcord.slash_command(name='clan_shop', description='magaz klana')
    async def clan_shop(self, interaction: nextcord.Interaction, clan_id: int):
        clan = await mogo.clans.find_one({'clan_id':clan_id})
        if clan != None:
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    title='MAGAZ',
                    description= str(role+'\n' for role in clan['clan_shop'])
                )
            )
        else:
            await interaction.response.send_message("Что то пошло не так... ")
    

    @nextcord.slash_command(name='clan_info', description='инфа про клан')
    async def clan_infoasd(self, interaction: nextcord.Interaction, clan_id: int):
        clan = await mogo.clans.find_one({'clan_id':clan_id})
        if clan != None:
            E = nextcord.Embed(
                title = f"{clan['clan_name']} clan",
                description=f"Владелец: <@{clan['owner_id']}>\nДенег накоплено: {clan['cash_clan']}\nКол-во участников: {len(clan['member'])}"
            )

            await interaction.response.send_message(embed=E)
        else:
            await interaction.response.send_message("Что то пошло не так... ")
        
    
    @nextcord.slash_command(name='clan_request_to_join', description='запрос на вступление в клан')
    async def clan_info(self, interaction: nextcord.Interaction, clan_id: int):
        clan = await mogo.clans.find_one({'clan_id':clan_id})
        if clan != None:
            owner = interaction.guild.get_member(clan['owner_id'])
            await owner.send(f"Пользователь {interaction.user.mention} создает запрос на вступление в клан {clan['clan_name']}")
            await interaction.response.send_message(f"Заявка отправлена")
        else:
            await interaction.response.send_message("Что то пошло не так... ")

            

def setup(bot):
    bot.add_cog(CCommands(bot))