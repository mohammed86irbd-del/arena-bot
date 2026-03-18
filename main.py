# ===================================
#        ARENA BOT - الكود الكامل
#         نسخة مصلحة ✅ + 24/7
# ===================================

import discord
from discord.ext import commands
from discord import app_commands
from collections import defaultdict
import asyncio, random, time, datetime
from flask import Flask
from threading import Thread

# ══════════════════════════════════════════════════
#           KEEP ALIVE - تشغيل 24/7
# ══════════════════════════════════════════════════

app = Flask('')

@app.route('/')
def home():
    return """
    <html><body style="background:#1e1e2e;color:#cdd6f4;font-family:sans-serif;text-align:center;padding:50px">
        <h1>⚔️ Arena Bot</h1>
        <p style="color:#a6e3a1">✅ البوت شغال وأونلاين!</p>
    </body></html>
    """

@app.route('/health')
def health():
    return {"status": "online", "bot": "Arena Bot ⚔️"}

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()
    print("🌐 Keep-Alive Server شغال على port 8080")

# ── إعداد البوت ──────────────────────────────────
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# ── بيانات الأسئلة ───────────────────────────────
questions = {
    "easy": [
        {"question": "ما هو نادي كريستيانو رونالدو حالياً؟",               "answer": "النصر"},
        {"question": "كم مرة فاز ميسي بالكرة الذهبية؟",                    "answer": "8"},
        {"question": "من فاز بكأس العالم 2022؟",                           "answer": "الأرجنتين"},
        {"question": "ما لون قميص المنتخب البرازيلي؟",                     "answer": "أصفر"},
    ],
    "medium": [
        {"question": "من فاز بدوري أبطال أوروبا 2022؟",                    "answer": "ريال مدريد"},
        {"question": "في أي مدينة يلعب نادي برشلونة؟",                     "answer": "برشلونة"},
        {"question": "كم عدد لاعبي كرة القدم في الملعب من فريقين؟",        "answer": "22"},
        {"question": "ما هو اسم كأس أوروبا؟",                              "answer": "يورو"},
    ],
    "hard": [
        {"question": "كم هدفاً سجل رونالدو في دوري أبطال أوروبا؟",         "answer": "140"},
        {"question": "في أي عام أسس نادي ريال مدريد؟",                    "answer": "1902"},
        {"question": "من هو أصغر لاعب يسجل في كأس العالم؟",               "answer": "بيليه"},
        {"question": "ما هو الرقم القياسي لأغلى صفقة في التاريخ؟",        "answer": "222 مليون"},
    ]
}

players_data = [
    {"name": "كريستيانو رونالدو", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cristiano_Ronaldo_2018.jpg/800px-Cristiano_Ronaldo_2018.jpg"},
    {"name": "ليونيل ميسي",       "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup.jpg"},
    {"name": "نيمار",              "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Neymar_-_2018_%28cropped%29.jpg/800px-Neymar_-_2018_%28cropped%29.jpg"},
]

countries = [
    {"name": "السعودية",  "emoji": "🇸🇦", "secret": False},
    {"name": "اليابان",   "emoji": "🇯🇵", "secret": False},
    {"name": "البرازيل",  "emoji": "🇧🇷", "secret": False},
    {"name": "إسبانيا",   "emoji": "🇪🇸", "secret": False},
    {"name": "إيطاليا",   "emoji": "🇮🇹", "secret": False},
    {"name": "الأرجنتين", "emoji": "🇦🇷", "secret": False},
    {"name": "فرنسا",     "emoji": "🇫🇷", "secret": False},
    {"name": "ألمانيا",   "emoji": "🇩🇪", "secret": False},
    {"name": "أتلانتس",   "emoji": "🌊",  "secret": True},
    {"name": "شنغريلا",   "emoji": "🏔️", "secret": True},
]

# ── متغيرات عامة ─────────────────────────────────
mafia_games    = {}
tournaments    = {}
spam_tracker   = defaultdict(list)
join_tracker   = []
user_passports = {}
scores         = defaultdict(int)

SPAM_LIMIT  = 5
SPAM_WINDOW = 5
RAID_LIMIT  = 10
RAID_WINDOW = 15

# ══════════════════════════════════════════════════
#              EVENTS - أحداث البوت
# ══════════════════════════════════════════════════

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"✅ Arena Bot جاهز! | تم تفعيل {len(synced)} أمر")
    await bot.change_presence(activity=discord.Game(name="⚔️ /quiz | /mafia | /travel"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
    now = time.time()
    uid = message.author.id
    spam_tracker[uid] = [t for t in spam_tracker[uid] if now - t < SPAM_WINDOW]
    spam_tracker[uid].append(now)
    if len(spam_tracker[uid]) >= SPAM_LIMIT:
        try:
            await message.author.timeout(
                discord.utils.utcnow() + datetime.timedelta(minutes=5),
                reason="🚨 كشف سبام تلقائي"
            )
            await message.channel.send(
                f"🛡️ تم كتم {message.author.mention} 5 دقائق بسبب السبام.",
                delete_after=10
            )
        except:
            pass
        spam_tracker[uid].clear()

@bot.event
async def on_member_join(member):
    now = time.time()
    global join_tracker
    join_tracker = [t for t in join_tracker if now - t < RAID_WINDOW]
    join_tracker.append(now)
    if len(join_tracker) >= RAID_LIMIT:
        try:
            await member.guild.edit(verification_level=discord.VerificationLevel.high)
            log_ch = discord.utils.get(member.guild.channels, name="logs")
            if log_ch:
                await log_ch.send("⚠️ **تحذير ريد!** تم رفع مستوى التحقق تلقائياً.")
        except:
            pass
    if member.bot:
        allowed_bots = []
        if member.id not in allowed_bots:
            try:
                await member.kick(reason="🤖 بوت غير مصرح")
            except:
                pass

# ══════════════════════════════════════════════════
#             GAMES COMMANDS - الألعاب
# ══════════════════════════════════════════════════

@bot.tree.command(name="quiz", description="⚽ ابدأ كويز كرة قدم تفاعلي!")
@app_commands.describe(difficulty="مستوى الصعوبة")
@app_commands.choices(difficulty=[
    app_commands.Choice(name="سهل 🟢",    value="easy"),
    app_commands.Choice(name="متوسط 🟡", value="medium"),
    app_commands.Choice(name="صعب 🔴",    value="hard"),
])
async def quiz(interaction: discord.Interaction, difficulty: str = "medium"):
    await interaction.response.defer()
    q = random.choice(questions[difficulty])
    embed = discord.Embed(
        title="⚽ كويز كرة القدم",
        description=f"**{q['question']}**\n\nعندك **30 ثانية** للإجابة!",
        color=0x10b981
    )
    embed.set_footer(text=f"مستوى: {difficulty} | اكتب إجابتك في الشات")
    await interaction.followup.send(embed=embed)

    def check(m):
        return (m.channel == interaction.channel and
                m.content.strip().lower() == q['answer'].strip().lower())
    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        scores[msg.author.id] += 10
        win = discord.Embed(
            title="🏆 إجابة صحيحة!",
            description=f"{msg.author.mention} أجاب صح! +10 نقاط 🎉\n**الإجابة:** {q['answer']}",
            color=0xf59e0b
        )
        await interaction.channel.send(embed=win)
    except asyncio.TimeoutError:
        await interaction.channel.send(f"⏱️ انتهى الوقت! الإجابة كانت: **{q['answer']}**")

@bot.tree.command(name="guess", description="🖼️ خمّن اللاعب من الصورة!")
async def guess_player(interaction: discord.Interaction):
    await interaction.response.defer()
    player = random.choice(players_data)
    embed = discord.Embed(
        title="🖼️ من هذا اللاعب؟",
        description="عندك **45 ثانية** لتخمين اسم اللاعب!",
        color=0x7c3aed
    )
    embed.set_image(url=player['image_url'])
    await interaction.followup.send(embed=embed)

    def check(m):
        return (m.channel == interaction.channel and
                m.content.strip().lower() == player['name'].strip().lower())
    try:
        msg = await bot.wait_for('message', check=check, timeout=45.0)
        scores[msg.author.id] += 15
        win = discord.Embed(
            title="🏆 صح!",
            description=f"{msg.author.mention} عرف اللاعب! +15 نقطة 🎉\n**هو:** {player['name']}",
            color=0xf59e0b
        )
        await interaction.channel.send(embed=win)
    except asyncio.TimeoutError:
        await interaction.channel.send(f"⏱️ انتهى الوقت! اللاعب كان: **{player['name']}**")

# ══════════════════════════════════════════════════
#              MAFIA - لعبة المافيا
# ══════════════════════════════════════════════════

@bot.tree.command(name="mafia", description="🕵️ لعبة المافيا التفاعلية")
@app_commands.describe(action="العملية")
@app_commands.choices(action=[
    app_commands.Choice(name="بدء لعبة جديدة", value="start"),
    app_commands.Choice(name="انضمام",          value="join"),
    app_commands.Choice(name="تشغيل اللعبة",    value="play"),
])
async def mafia(interaction: discord.Interaction, action: str):
    await interaction.response.defer()
    gid = interaction.guild.id

    if action == "start":
        mafia_games[gid] = {'players': [], 'started': False}
        embed = discord.Embed(
            title="🕵️ لعبة المافيا",
            description="استخدم `/mafia join` للانضمام!\n✅ تحتاج **4 لاعبين** على الأقل.\nبعدها استخدم `/mafia play` لبدء اللعبة.",
            color=0x1e1e2e
        )
        await interaction.followup.send(embed=embed)

    elif action == "join":
        if gid not in mafia_games:
            await interaction.followup.send("❌ ما في لعبة! استخدم `/mafia start` أولاً")
            return
        g = mafia_games[gid]
        if interaction.user in g['players']:
            await interaction.followup.send("❌ أنت مسجل مسبقاً!")
            return
        g['players'].append(interaction.user)
        await interaction.followup.send(
            f"✅ {interaction.user.mention} انضم للعبة! ({len(g['players'])} لاعب)"
        )

    elif action == "play":
        if gid not in mafia_games:
            await interaction.followup.send("❌ ما في لعبة! استخدم `/mafia start` أولاً")
            return
        g = mafia_games[gid]
        if len(g['players']) < 4:
            await interaction.followup.send(f"❌ يلزم 4 لاعبين على الأقل! الحالي: {len(g['players'])}")
            return
        players = g['players'].copy()
        random.shuffle(players)
        n       = len(players)
        mafia_n = max(1, n // 4)
        roles   = ['مافيا'] * mafia_n + ['محقق'] + ['مواطن'] * (n - mafia_n - 1)
        random.shuffle(roles)
        for i, player in enumerate(players):
            role  = roles[i]
            emoji = "🔫" if role == "مافيا" else ("🔍" if role == "محقق" else "👤")
            color = 0xef4444 if role == "مافيا" else (0x3b82f6 if role == "محقق" else 0x10b981)
            desc  = ("🔫 مهمتك قتل المواطنين دون أن تُكشف!" if role == "مافيا"
                     else ("🔍 مهمتك كشف المافيا!" if role == "محقق"
                           else "👤 مهمتك كشف المافيا والبقاء حياً!"))
            try:
                dm = discord.Embed(
                    title="🕵️ دورك في المافيا",
                    description=f"أنت: **{emoji} {role}**\n\n{desc}",
                    color=color
                )
                await player.send(embed=dm)
            except:
                pass
        embed = discord.Embed(
            title="🕵️ اللعبة بدأت!",
            description=f"تم توزيع الأدوار على **{n} لاعبين** سراً ✅\n\n🔫 المافيا: **{mafia_n}**\n🔍 المحقق: **1**\n👤 المواطنين: **{n - mafia_n - 1}**\n\n📩 كل لاعب وصله دوره في الخاص!",
            color=0x7c3aed
        )
        await interaction.followup.send(embed=embed)
        mafia_games[gid]['started'] = True

# ══════════════════════════════════════════════════
#           TOURNAMENT - نظام البطولات
# ══════════════════════════════════════════════════

@bot.tree.command(name="tournament", description="🏆 نظام البطولات")
@app_commands.describe(action="العملية", name="اسم البطولة")
@app_commands.choices(action=[
    app_commands.Choice(name="إنشاء بطولة", value="create"),
    app_commands.Choice(name="انضمام",       value="join"),
    app_commands.Choice(name="بدء البطولة",  value="start"),
    app_commands.Choice(name="عرض القوس",    value="bracket"),
])
async def tournament(interaction: discord.Interaction, action: str, name: str = ""):
    await interaction.response.defer()
    gid = interaction.guild.id

    if action == "create":
        if not name:
            await interaction.followup.send("❌ أدخل اسم البطولة!")
            return
        tournaments[gid] = {'name': name, 'players': [], 'started': False}
        embed = discord.Embed(
            title=f"🏆 بطولة جديدة: {name}",
            description="استخدم `/tournament join` للانضمام!\nبعد اكتمال اللاعبين استخدم `/tournament start`",
            color=0xf59e0b
        )
        await interaction.followup.send(embed=embed)

    elif action == "join":
        t = tournaments.get(gid)
        if not t:
            await interaction.followup.send("❌ ما في بطولة! استخدم `/tournament create`")
            return
        if t['started']:
            await interaction.followup.send("❌ البطولة بدأت مسبقاً!")
            return
        if interaction.user in t['players']:
            await interaction.followup.send("❌ أنت مسجل مسبقاً!")
            return
        t['players'].append(interaction.user)
        await interaction.followup.send(f"✅ {interaction.user.mention} انضم! ({len(t['players'])} لاعب)")

    elif action == "start":
        t = tournaments.get(gid)
        if not t or len(t['players']) < 2:
            await interaction.followup.send("❌ يلزم لاعبين على الأقل!")
            return
        random.shuffle(t['players'])
        t['started'] = True
        bracket_txt = ""
        players = t['players']
        for i in range(0, len(players), 2):
            p1 = players[i].display_name
            p2 = players[i+1].display_name if i+1 < len(players) else "🏅 BYE"
            bracket_txt += f"⚔️ `{p1}` **vs** `{p2}`\n"
        embed = discord.Embed(
            title=f"🏆 قوس بطولة: {t['name']}",
            description=bracket_txt,
            color=0xf59e0b
        )
        await interaction.followup.send(embed=embed)

    elif action == "bracket":
        t = tournaments.get(gid)
        if not t:
            await interaction.followup.send("❌ ما في بطولة!")
            return
        names = "\n".join([f"• {p.display_name}" for p in t['players']]) or "لا يوجد لاعبين بعد"
        embed = discord.Embed(
            title=f"🏆 {t['name']} - المسجلون ({len(t['players'])} لاعب)",
            description=names,
            color=0xf59e0b
        )
        await interaction.followup.send(embed=embed)

# ══════════════════════════════════════════════════
#              TRAVEL - نظام السفر
# ══════════════════════════════════════════════════

@bot.tree.command(name="travel", description="🌍 نظام السفر حول العالم")
@app_commands.describe(action="العملية", destination="اسم الدولة للزيارة")
@app_commands.choices(action=[
    app_commands.Choice(name="جواز سفري",    value="passport"),
    app_commands.Choice(name="زيارة دولة",   value="visit"),
    app_commands.Choice(name="دولة سرية 🔒", value="secret"),
    app_commands.Choice(name="قائمة الدول",  value="list"),
])
async def travel(interaction: discord.Interaction, action: str, destination: str = ""):
    await interaction.response.defer()
    uid = interaction.user.id
    if uid not in user_passports:
        user_passports[uid] = {'stamps': [], 'secrets': 0}
    passport = user_passports[uid]

    if action == "passport":
        stamps_txt = " ".join(passport['stamps']) if passport['stamps'] else "لا يوجد طوابع بعد ✈️"
        embed = discord.Embed(title=f"🛂 جواز سفر {interaction.user.display_name}", color=0x06b6d4)
        embed.add_field(name="🗺️ الطوابع",          value=stamps_txt,                   inline=False)
        embed.add_field(name="✈️ الدول المزارة",     value=str(len(passport['stamps'])), inline=True)
        embed.add_field(name="🔮 الأسرار المكتشفة", value=str(passport['secrets']),     inline=True)
        await interaction.followup.send(embed=embed)

    elif action == "visit":
        if not destination:
            await interaction.followup.send("❌ اكتب اسم الدولة في خانة destination!")
            return
        country = next((c for c in countries if c['name'] == destination and not c['secret']), None)
        if not country:
            await interaction.followup.send("❌ دولة غير موجودة! استخدم `/travel list` لرؤية الدول.")
            return
        stamp = country['emoji']
        if stamp not in passport['stamps']:
            passport['stamps'].append(stamp)
            embed = discord.Embed(
                title=f"✈️ مرحباً في {country['name']}!",
                description=f"حصلت على طابع {stamp} في جواز سفرك! 🎉",
                color=0x10b981
            )
        else:
            embed = discord.Embed(
                title=f"{country['emoji']} {country['name']}",
                description="زرت هذه الدولة من قبل! جرب دولة جديدة 🌍",
                color=0xf59e0b
            )
        await interaction.followup.send(embed=embed)

    elif action == "secret":
        if len(passport['stamps']) < 5:
            await interaction.followup.send(
                f"🔒 تحتاج زيارة **5 دول** أولاً!\nأنت زرت: **{len(passport['stamps'])}** دول"
            )
            return
        secret_countries = [c for c in countries if c['secret']]
        secret = random.choice(secret_countries)
        passport['secrets'] += 1
        embed = discord.Embed(
            title="🔮 اكتشفت دولة سرية!",
            description=f"**{secret['name']} {secret['emoji']}**\nهذا المكان الآن في جوازك! 🌟",
            color=0x7c3aed
        )
        await interaction.followup.send(embed=embed)

    elif action == "list":
        visible = [c for c in countries if not c['secret']]
        txt = "\n".join([f"{c['emoji']} {c['name']}" for c in visible])
        embed = discord.Embed(
            title="🌍 الدول المتاحة للزيارة",
            description=txt + "\n\n🔒 + دول سرية تُكتشف بعد زيارة 5 دول!",
            color=0x06b6d4
        )
        await interaction.followup.send(embed=embed)

# ══════════════════════════════════════════════════
#              TICKETS - نظام التذاكر
# ══════════════════════════════════════════════════

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 إغلاق التذكرة", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.channel.send("🔒 جاري إغلاق التذكرة...")
        await asyncio.sleep(2)
        await interaction.channel.delete()

class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 فتح تذكرة", style=discord.ButtonStyle.primary, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        guild    = interaction.guild
        existing = discord.utils.get(guild.channels, name=f"ticket-{interaction.user.name}")
        if existing:
            await interaction.followup.send(f"❌ عندك تذكرة مفتوحة: {existing.mention}", ephemeral=True)
            return
        category = discord.utils.get(guild.categories, name="🎫 التذاكر")
        if not category:
            category = await guild.create_category("🎫 التذاكر")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user:   discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}", category=category, overwrites=overwrites
        )
        embed = discord.Embed(
            title="🎫 تذكرة جديدة",
            description=f"أهلاً {interaction.user.mention}!\nاكتب مشكلتك وسيرد عليك الدعم قريباً. 🙏",
            color=0x7c3aed
        )
        await channel.send(embed=embed, view=CloseTicketView())
        await interaction.followup.send(f"✅ تم فتح تذكرتك: {channel.mention}", ephemeral=True)

@bot.tree.command(name="ticket", description="🎫 إنشاء لوحة التذاكر")
@app_commands.checks.has_permissions(administrator=True)
async def ticket_panel(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="🎫 نظام الدعم",
        description="اضغط الزر أدناه لفتح تذكرة دعم.\nسيرد عليك فريق الإدارة في أقرب وقت. 💜",
        color=0x7c3aed
    )
    await interaction.followup.send(embed=embed, view=TicketButton())

# ══════════════════════════════════════════════════
#           MODERATION - أوامر الإدارة
# ══════════════════════════════════════════════════

@bot.tree.command(name="ban", description="🔨 حظر عضو")
@app_commands.describe(member="العضو", reason="السبب")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    await interaction.response.defer()
    await member.ban(reason=reason)
    embed = discord.Embed(
        title="🔨 تم الحظر",
        description=f"تم حظر {member.mention}\n**السبب:** {reason}",
        color=0xef4444
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="kick", description="👢 طرد عضو")
@app_commands.describe(member="العضو", reason="السبب")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    await interaction.response.defer()
    await member.kick(reason=reason)
    embed = discord.Embed(
        title="👢 تم الطرد",
        description=f"تم طرد {member.mention}\n**السبب:** {reason}",
        color=0xf59e0b
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="mute", description="🔇 كتم عضو مؤقتاً")
@app_commands.describe(member="العضو", minutes="المدة بالدقائق", reason="السبب")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, minutes: int = 10, reason: str = "لا يوجد سبب"):
    await interaction.response.defer()
    await member.timeout(
        discord.utils.utcnow() + datetime.timedelta(minutes=minutes),
        reason=reason
    )
    embed = discord.Embed(
        title="🔇 تم الكتم",
        description=f"تم كتم {member.mention} لمدة **{minutes} دقيقة**\n**السبب:** {reason}",
        color=0xf59e0b
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="purge", description="🗑️ حذف رسائل")
@app_commands.describe(amount="عدد الرسائل")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int = 10):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"🗑️ تم حذف **{len(deleted)}** رسالة.", ephemeral=True)

@bot.tree.command(name="lockdown", description="🔒 قفل السيرفر - وضع الطوارئ")
@app_commands.checks.has_permissions(administrator=True)
async def lockdown(interaction: discord.Interaction):
    await interaction.response.defer()
    for channel in interaction.guild.channels:
        try:
            await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        except:
            pass
    embed = discord.Embed(
        title="🔒 تم قفل السيرفر",
        description="السيرفر في وضع الطوارئ 🚨\nاستخدم `/unlock` لإلغاء القفل.",
        color=0xef4444
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="unlock", description="🔓 فتح السيرفر")
@app_commands.checks.has_permissions(administrator=True)
async def unlock(interaction: discord.Interaction):
    await interaction.response.defer()
    for channel in interaction.guild.channels:
        try:
            await channel.set_permissions(interaction.guild.default_role, send_messages=True)
        except:
            pass
    embed = discord.Embed(
        title="🔓 تم فتح السيرفر",
        description="السيرفر عاد للعمل الطبيعي ✅",
        color=0x10b981
    )
    await interaction.followup.send(embed=embed)

# ══════════════════════════════════════════════════
#           LEADERBOARD - الترتيب والنقاط
# ══════════════════════════════════════════════════

@bot.tree.command(name="leaderboard", description="🏅 ترتيب اللاعبين بالنقاط")
async def leaderboard(interaction: discord.Interaction):
    await interaction.response.defer()
    if not scores:
        await interaction.followup.send("📊 لا يوجد نقاط بعد! العب `/quiz` أو `/guess` لتكسب نقاط 🎮")
        return
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    desc   = ""
    for i, (uid, pts) in enumerate(sorted_scores):
        user = interaction.guild.get_member(uid)
        name = user.display_name if user else "لاعب مجهول"
        desc += f"{medals[i]} **{name}** — {pts} نقطة\n"
    embed = discord.Embed(title="🏆 ترتيب اللاعبين", description=desc, color=0xf59e0b)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="score", description="⭐ اعرض نقاطك الشخصية")
async def score(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    pts = scores.get(interaction.user.id, 0)
    embed = discord.Embed(
        title=f"⭐ نقاط {interaction.user.display_name}",
        description=f"عندك **{pts} نقطة** 🎮\nالعب أكثر لترتفع في الترتيب!",
        color=0x7c3aed
    )
    await interaction.followup.send(embed=embed, ephemeral=True)

# ══════════════════════════════════════════════════
#                   RUN THE BOT
# ══════════════════════════════════════════════════

keep_alive()   # ✅ تشغيل السيرفر للـ 24/7

# ===================================
# 🔑 ضع توكنك هنا ↓↓↓
TOKEN = "ضع_توكنك_هنا"
# ===================================
bot.run(TOKEN)
