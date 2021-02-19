import re
import os
import logging
import sys

RE_MARKDOWN_IMG_URL_PATTERN = re.compile("!\\[.*?\\]\\((.*?)\\)|<img.*?src=['\"](.*?)['\"].*?>")
RE_URL_PATTREN = re.compile("((http(s?))|(ftp))://.*")
CHARSET = "utf-8"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

total = 0
ignore = 0


def isImg(filename):
    pass


def transfer_online_img(filename):
    pass


def md_img_find(md_file):
    """
    将给定的markdown文件里的图片本地路径转换成网上路径
    """

    text = None
    logger.info("文件名：", md_file)
    with open(md_file, "r", encoding=CHARSET) as f:
        global total, ignore
        text = f.read()
        matches = RE_MARKDOWN_IMG_URL_PATTERN.findall(text)
        if matches:
            for match in matches:
                if match:
                    logger.info(f"匹配路径 :{match} ")
                    if RE_URL_PATTREN.match(match):
                        loc_p = match
                        if not os.path.exists(loc_p) or not os.path.isfile(loc_p):
                            loc_p = md_file[: md_file.rfind("\\") + 1] + match
                        if os.path.exists(loc_p) and os.path.isfile(loc_p):
                            # 如果是一个图片的话，才要上传，否则的话，不用管
                            if isImg(loc_p):
                                pass
                            else:
                                ignore = ignore + 1
                                logger.info(f"不是一个图片文件 ：{loc_p}")
                                continue
                        else:
                            ignore = ignore + 1
                            logger.info(f" 文件不存在 ：{loc_p}")
                    else:
                        logger.info(f"本地地址：{match}")
                        file_url = transfer_online_img(match)
                        if file_url:
                            logger.info(f"图片地址是 ：{file_url}")
                            # post = post.replace(match, file_url)


def main(args):
    filepath = os.path.abspath(args[1])
    logger.info(f"文件路径：{filepath}")
    md_img_find(filepath)


if __name__ == "__main__":
    main(sys.argv)
