import os
os.system("pip install pyrubi")
from pyrubi import Client
from threading import Thread

bot = Client("acc2")
Guid_map = []

def target_link(m):
    send = m.reply("please waiting . . .")
    Guid_map.clear()
    if "joinc" in m.text :
        Guid = bot.get_chat_preview(m.text.split("/link")[1].strip())["channel"]["channel_guid"]
        Guid_map.append(Guid)
        m.reply("saved channel upload .")
    elif "@" in m.text :
        Guid = bot.get_chat_info_by_username(m.text.split("/link")[1].strip())["channel"]["channel_guid"]
        Guid_map.append(Guid)
        m.reply("saved channel upload .")
    bot.delete_messages(m.author_guid,[send["message_update"]["message_id"]])

def upload(m):
    if len(Guid_map) == 0 :
        m.reply("not map link !")
    else:
        send = m.reply("please waiting . . .")
        if m.reply_message_id != None:
            types = bot.get_messages(m.object_guid, m.reply_message_id)["messages"][0]["file_inline"]["type"]
            dlink = bot.get_download_link(m.author_guid, m.reply_message_id)
            if types == "Music":
                bot.send_music(Guid_map[0], file=dlink, file_name="music-rubika")
            elif types == "Image":
                bot.send_image(Guid_map[0], file=dlink)
            elif types == "Video":
                bot.send_video(Guid_map[0], file=dlink)
            elif types == "File":
                bot.send_file(Guid_map[0], file=dlink, file_name="File.mp4")
            m.reply(f"{types} Uploadd  .")
        bot.delete_messages(m.author_guid,[send["message_update"]["message_id"]])

for m in bot.on_message():
    try:
        if m.text.startswith("/upload"):
            Thread(target=upload, args=[m]).start()
        elif m.text.startswith("/link"):
            Thread(target=target_link, args=[m]).start()
    except Exception as e:
        m.reply("error :\n\n "+str(e))
