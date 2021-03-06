from operator import itemgetter

import discord

from Arcapi import AsyncApi

from constants import partners_names
from utils import check_id, get_partner_icon, format_time, format_code

async def profile(message):
    code = await check_id(message.author.id)
    if not code:
        await message.channel.send("> Erreur: Aucun code Arcaea n'est lié a ce compte Discord (*!register*)")
        return

    api_ = AsyncApi(user_code=code)
    data = await api_.scores()
    prfl = data[1]

    ls_top = []
    for elm in data[2:]:
        ls_top.append(elm)

    ls_top = sorted(ls_top, key=itemgetter("rating"), reverse=True)[0:30]

    b30 = 0.0
    for elm in ls_top:
        b30 += elm['rating']
    b30 /= 30
    r10 = prfl['rating'] * 0.04 - b30 * 3

    b30f = "{:.3f}".format(b30)
    r10f = "{:.3f}".format(r10)

    rating = "{0:04d}".format(prfl["rating"])[:2] + "." + "{0:04d}".format(prfl["rating"])[2:] + " PTT"

    if rating == "-0.01 PTT":
        rating = "*Hidden*"

    msg_emb = discord.Embed(title="Profile", type="rich", color=discord.Color.dark_teal())
    msg_emb.set_thumbnail(url=get_partner_icon(prfl))
    msg_emb.add_field(name=f'**{prfl["name"]}\'s profile**',
                      value=f'> Rating: **{rating}**\n'
                            f'> Best 30: **{b30f} PTT**\n'
                            f'> Recent 10: **{r10f} PTT**\n'
                            f'> Favchar: **{partners_names[prfl["character"]]}**\n'
                            f'> Last play: **{format_time(prfl["recent_score"][0]["time_played"])}**\n'
                            f'> Join date: **{format_time(prfl["join_date"])}**\n'
                            f'> Code: **{format_code(code)}**')
    await message.channel.send(embed=msg_emb)
