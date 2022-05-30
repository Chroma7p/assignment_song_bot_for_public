import discord
import textwrap
from discord.ext import commands

"""借りた:https://gist.github.com/coolwind0202/e4efebdeda499d4498782b194f2d9be2#file-base-py"""

TOKEN = 'ここにトークンを入れる'


class Help(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "カテゴリ未設定"
        self.command_attrs["description"] = "このメッセージを表示します。"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"

    async def create_category_tree(self,category,enclosure):
        """
        コマンドの集まり（Group、Cog）から木の枝状のコマンドリスト文字列を生成する。
        生成した文字列は enlosure 引数に渡された文字列で囲われる。
        """
        content = ""
        command_list = category.walk_commands()
        for cmd in await self.filter_commands(command_list,sort=True):
            if cmd.root_parent:
                # cmd.root_parent は「根」なので、根からの距離に応じてインデントを増やす
                index = cmd.parents.index(cmd.root_parent)
                indent = "\t" * (index + 1)
                if indent:
                    content += f"{indent}- {cmd.name} / {cmd.description}\n"
                else:
                    # インデントが入らない、つまり木の中で最も浅く表示されるのでprefixを付加
                    content += f"{self.context.prefix}{cmd.name} / {cmd.description}\n"
            else:
                # 親を持たないコマンドなので、木の中で最も浅く表示する。prefixを付加
                content += f"{self.context.prefix}{cmd.name} / {cmd.description}\n"
        
        return enclosure + textwrap.dedent(content) + enclosure

    async def send_bot_help(self,mapping):
        embed = discord.Embed(title="helpコマンド",color=0x000000)
        if self.context.bot.description:
            # もしBOTに description 属性が定義されているなら、それも埋め込みに追加する
            embed.description = self.context.bot.description
        for cog in mapping:
            if cog:
                cog_name = cog.qualified_name
            else:
                # mappingのキーはNoneになる可能性もある
                # もしキーがNoneなら、自身のno_category属性を参照する
                cog_name = self.no_category
        
            command_list = await self.filter_commands(mapping[cog],sort=True)
            content = ""
            for cmd in command_list:
                content += f"`{self.context.prefix}{cmd.name}`\n {cmd.description}\n"
            embed.add_field(name=cog_name,value=content,inline=False)

        await self.get_destination().send(embed=embed)
        
    async def send_cog_help(self,cog):
        embed = discord.Embed(title=cog.qualified_name,description=cog.description,color=0x00ff00)
        embed.add_field(name="コマンドリスト：",value=await self.create_category_tree(cog,"```"))
        await self.get_destination().send(embed=embed)

    async def send_group_help(self,group):
        embed = discord.Embed(title=f"{self.context.prefix}{group.qualified_name}",
            description=group.description,color=0x000000)
        if group.aliases:
            embed.add_field(name="有効なエイリアス：",value="`" + "`, `".join(group.aliases) + "`",inline=False)
        if group.help:
            embed.add_field(name="ヘルプテキスト：",value=group.help,inline=False)
        embed.add_field(name="サブコマンドリスト：",value=await self.create_category_tree(group,"```"),inline=False)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self,command):
        params = " ".join(command.clean_params.keys())
        embed = discord.Embed(title=f"{self.context.prefix}{command.qualified_name} {params}",
            description=command.description,color=0x000000)
        if command.aliases:
            embed.add_field(name="有効なエイリアス：",value="`" + "`, `".join(command.aliases) + "`",inline=False)
        if command.help:
            embed.add_field(name="ヘルプテキスト：",value=command.help,inline=False)
        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="ヘルプ表示のエラー",description=error,color=0xff0000)
        await self.get_destination().send(embed=embed)

    def command_not_found(self,string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self,command,string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            # もし、そのコマンドにサブコマンドが存在しているなら
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"

dscrpt="""定数指定方法
xx.x:直接指定
xx.x~xx.x:範囲指定
xx.x~:下限指定
rxx.x:目標レート値指定、譜面に加えて目標スコアを提示(基本的に最大の定数+2まで)"""

bot=commands.Bot(command_prefix='!',help_command=Help(),description=dscrpt)
cogfolder="cogs."
cogs=["gekicog",
      "chucog",
      "maicog",
      "noscog",
      "searchcog",
      #"mycog",
      ]

for c in cogs:
  bot.load_extension(cogfolder+c)





@bot.event
async def on_ready():
    print("Hello!")
    await bot.change_presence(activity=discord.Game(name="!helpでヘルプを表示   ", type=1))

bot.run(TOKEN)