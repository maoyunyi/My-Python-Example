import requests
from bs4 import BeautifulSoup
import re
import time


headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42"
}


def main():
    start_time = time.time()
    for number in range(1,149):
        print('获取文章地址:' + '第' + str(number) + '篇')
        html = 'https://nine-lie.com/'
        html = html + "category/浮生取义/page/" + str(number)
        page = requests.get(html, headers=headers)
        first_soup = BeautifulSoup(page.text, 'lxml')
        title = first_soup.h2.a
        href = re.search("([a-zA-z]+://[^\s]*/)", str(title))
        get_html = href.group(1)
        print('获取正文:' + '第' + str(number) + '篇')
        second_page = requests.get(get_html)
        second_soup = BeautifulSoup(second_page.text, 'lxml')
        post_time = second_soup.find(name='time')
        post_time = post_time.text
        contents = second_soup.find_all(class_='iriska-single-post-content')
        comments_title = second_soup.find_all(class_='iriska-comments-title')
        for i in comments_title:
            comments_title = str(i.text).strip()
            comments_title = re.match('([A-Z])\w(.*\d).', comments_title)
            if str(type(comments_title)) == "<class 're.Match'>":
                comments_title = comments_title.group()
            else:
                comments_title = "无评论"
        comments = second_soup.find_all(class_='comment-content')
        print('写入正文:' + '第' + str(number) + '篇')
        with open('nine_line_blog.txt', 'a', encoding="utf-8") as f:
            f.write('=' * 50 + '\n')
            f.write('标题:'+ title.text + '\n' + '日期:'+post_time + '\n')
            f.write('正文:\n')
            for content in contents:
                content = content.find_all('p')
                for i in content:
                    text = i.text
                    f.write(str(text))
                    f.write('\n')
            f.write('\n')
            if comments_title:                f.write(comments_title)
            f.write('\n')
            for comment in comments:
                comment = comment.find_all('p')
                for i in comment:
                    text = i.text
                    f.write(str(text))
                    f.write('\n')
            f.write('=' * 50)
            end_time = time.time()
            print('已完成 {:.2%}:'.format((number / 148)))
    print('写入txt完成')
    print('花费了 %.4s 秒' % (float(end_time - start_time)))


if __name__ == '__main__':
    main()
