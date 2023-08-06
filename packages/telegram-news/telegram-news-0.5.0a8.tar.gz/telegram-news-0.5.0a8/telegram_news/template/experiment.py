import os
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from telegram_news.template.common import (
    NewsPostman,
    InfoExtractor,
)

channel = os.getenv("CHANNEL")

if __name__ == '__main__':

    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    db = Session(bind=conn)

    tgtg = NewsPostman(listURLs=['https://t.me/s/telegram'], sendList=[channel], db=db, tag='TgTg')
    tgtgIE = InfoExtractor()

    def tgtglpp(text):
        # text = text.replace('<br/>', '\n')
        def rep(matchobj):
            return '</a><time>' + re.findall(r'\d+.\d+.\d+.\d+.\d+.\d+.\d+.\d+', matchobj.group(0))[0] + '</time><a>'
        return re.sub('<time datetime=".*?">.*?</time>', rep, text)

    tgtgIE.set_list_pre_process_policy(tgtglpp)
    tgtgIE.set_list_selector('div.tgme_widget_message_wrap')
    tgtgIE.set_outer_link_selector('a.tgme_widget_message_date')
    tgtgIE.set_outer_title_selector(None)
    tgtgIE.set_outer_paragraph_selector('div.tgme_widget_message_text')
    tgtgIE.set_outer_time_selector('time')
    # tgtgIE.set_outer_image_selector('img')
    # tgtgIE.set_outer_video_selector('video')
    tgtg.set_extractor(tgtgIE)
    tgtg.set_table_name('test')
    tgtg.enable_auto_retry()
    tgtgIE.keep_media_link()
    tgtg.poll()