import requests
import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
from config import urls
def send(message = False, embed_title = False, embed_description = False, file_path = False, username = "bot", server = "backtest_debug"):

    # backtest
    if server == "backtest":
        url = urls.discord_server_backtest
    if server == "backtest_debug":
        url = urls.discord_server_backtest_debug
    if server == "backtest_error":
        url = urls.discord_server_backtest_error

    # account
    if server == "database":
        url = urls.discord_server_database
    if server == "binance_report":
        url = urls.discord_server_binance_report
    if server == "binancetestnet_report":
        url = urls.discord_server_binancetestnet_report
    if server == "trade_debug":
        url = urls.discord_server_trade_debug

    # trading
    if server == "order_message":
        url = urls.discord_server_order_message
    if server == "trade_system_log":
        url = urls.discord_server_trade_system_log
    if server == "trade_system_error":
        url = urls.discord_server_trade_system_error

    # google cloud
    if server == "googleCloudStorage":
        url = urls.discord_server_googleCloudStorage
    if server == "vm":
        url = urls.discord_server_vm

    #_________________________________________________________________________

    if message and embed_title:
        embed = {
            "description": embed_description,
            "title": embed_title}
        data = {
            "content": message,
            "username": username,
            "embeds": [embed],}
        result = requests.post(url, json=data)

    elif message and not embed_title:
        data = {
            "content": message,
            "username": username,}
        result = requests.post(url, json=data)

    if file_path:
        with open(file_path, 'rb') as f:
            file_bin = f.read()
            files_qiita = {"favicon" : ( file_path, file_bin),}   
        result = requests.post(url, files = files_qiita)
    
    if 200 <= result.status_code < 300:
        print(f"Discord sent to {server} \
        message->{message} \
        embed_title->{embed_title} \
        embed_description->{embed_description}\
        file_path->{file_path}")
    else:
        print(f"ERROR Discord message...  {server} {result.status_code}, response:\n{result.json()}")

#________________________
if __name__ == "__main__":

    send(message = "hello")

"""
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TODO:

def complex_Didcord(message, embed_title, embed_description = "", file_path = False, username = "Daiki bot", server = "general"):
    URL = urls.discord_server_backtest_debug #debug server

    payload2 = {
        "payload_json" : {
            "username"      :username,
            "content"       : message,
            #"avatar_url"    : "https://github.com/qiita.png",
            "embeds": [
                {
                    "title"         : embed_title,
                    "description"   : embed_description,
                    #"url"           : "https://birdie0.github.io/discord-webhooks-guide/structure/file.html",
                    #"time_datastamp"     : "2020-08-22T15:18:00+0900",
                    "color"         : 5620992,
                    "footer": {
                        "icon_url"  : "attachment://test.jpg",
                        "text"      : "Qiita",
                    },
                    "thumbnail": {
                        "url"       : "attachment://test.jpg"
                    },
                    "image": {
                        "url"       : f"attachment://home/username/project/test.jpg"
                    },
                    "author": {
                        "name"      : "embedと。",
                        "url"       : "https://qiita.com/",
                        "icon_url"  : "attachment://test.jpg",
                    },
                    "video": {
                        "url"       : "https://www.youtube.com/embed/q05aeEf17Kc"
                    },
                    # "fields": [
                    #     {
                    #         "name"  : "添付画像を",
                    #         "value" : "embedsで使うと別表示しなくなるっぽい。",
                    #         "inline": True,
                    #     },
                    #     {
                    #         "name"  : "attachment:",
                    #         "value" : "embedの中でしか添付使えないっぽい。",
                    #         "inline": True,
                    #     },
                    #     {
                    #         "name"  : "Visualizer and validator for Discord embeds.",
                    #         "value" : "日本語入れたら怒らたけど、color pickerが地味に便利。",
                    #     },
                    #     {
                    #         "name"  : "Youtubeの",
                    #         "value" : "[埋め込みは無理っぽい](https://support.discord.com/hc/en-us/community/posts/360037387352-Videos-in-Rich-Embeds)\nvideo URL 指定しても無視される。",
                    #     },
                    # ],
                }
            ]
        }
    }

    ### embed付き
    with open("test.jpg", 'rb') as f:
        file_bin_favicon = f.read()
    with open("test.jpg", 'rb') as f:
        file_bin_logobg = f.read()
    with open("test.jpg", 'rb') as f:
        file_bin_logoeffect = f.read()

    files_qiita  = {
        "favicon" : ( "test.jpg", file_bin_favicon ),
        "logo_bg" : ( "test.jpg", file_bin_logobg ),
        "logo_effect" : ( "test.jpg", file_bin_logoeffect ),}

    payload2['payload_json'] = json.dumps( payload2['payload_json'], ensure_ascii=False )
    res = requests.post(URL, files = files_qiita  , data = payload2 )

    print( res.status_code )
    print( json.dumps( json.loads(res.content), indent=4, ensure_ascii=False ) )

# #________________________
# if __name__ == "__main__":
#     complex_Didcord("hey", "hohoho", file_path = '/home/username/project/test.jpg')
"""