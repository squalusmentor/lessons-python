# Урок B3.5 — BeautifulSoup: дерево, CSS-селекторы, текст и атрибуты
#
# Демо работает на встроённом HTML (структура как у kovrov-gorod.ru),
# чтобы не ходить в сеть. Живой сайт — в практике.
from bs4 import BeautifulSoup

HTML = """
<html>
<body>
  <div class="box-gallery"><h5>Последние новости</h5></div>
  <div id="newsbox">
    <div class="newsitem">
      <h3>В городе открыли новый парк</h3>
      <div class="pub-date">Опубликовано 9 Июня в 10:48</div>
      <a href="images/pic_news/101_b.jpg" rel="floatbox">
        <img src="/images/pic_news/101_s.jpg" width="125">
      </a>
      <p>Сегодня состоялось торжественное открытие...</p>
      <div class="nextnews"><a href="/press/news/101.html">подробнее &raquo;</a></div>
    </div>
    <div class="newsitem">
      <h3>Отключение воды на улице Ленина</h3>
      <div class="pub-date">Опубликовано 10 Июня в 08:15</div>
      <p>В связи с ремонтными работами...</p>
      <div class="nextnews"><a href="/press/news/102.html">подробнее &raquo;</a></div>
    </div>
    <div class="newsitem">
      <h3>Расписание автобусов изменится с июля</h3>
      <div class="pub-date">Опубликовано 11 Июня в 14:30</div>
      <p>Маршруты 2 и 7 переходят на летний график...</p>
      <div class="nextnews"><a href="/press/news/103.html">подробнее &raquo;</a></div>
    </div>
  </div>
</body>
</html>
"""


def demo5():
    soup = BeautifulSoup(HTML, "html.parser")

    print("-- select_one: первое совпадение или None --")
    header = soup.select_one("div.box-gallery h5")
    print("  заголовок блока:", header.text)
    missing = soup.select_one("div.no-such-class")
    print("  несуществующий селектор ->", missing)

    print("-- select: все совпадения (список) --")
    titles = soup.select("#newsbox div.newsitem h3")
    print("  найдено заголовков:", len(titles))
    for i, tag in enumerate(titles, 1):
        print(f"  {i}. {tag.get_text(strip=True)}")

    print("-- атрибуты: tag['href'] и tag.get(...) --")
    for link in soup.select("div.nextnews a"):
        print("  href =", link["href"], "| текст =", link.get_text(strip=True))
    img = soup.select_one("div.newsitem img")
    print("  img.get('width') =", img.get("width"))
    print("  img.get('alt')   =", img.get("alt"))      # нет атрибута -> None

    print("-- селектор по атрибуту --")
    floatbox = soup.select("a[rel=floatbox]")
    print("  ссылок с rel=floatbox:", len(floatbox))

    print("-- комбинируем: дата конкретной новости --")
    second = soup.select("div.newsitem")[1]
    print("  вторая новость:", second.select_one("h3").text)
    print("  её дата:", second.select_one(".pub-date").text)


if __name__ == "__main__":
    demo5()
