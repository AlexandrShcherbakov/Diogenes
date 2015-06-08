<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{query}} | Diogenes</title>
    <link href="/static/styles.css" rel="stylesheet">
  </head>
  <body class="content_area">
    <div id="menu">
      <img src="/static/logo.png" id="logo">
      <form>
        <input type="text" autofocus name="query" value="{{query}}">
        <button>Search</button>
      </form>
    </div>
% if modif:
    <div class="info">
    Ваш запрос "{{modif}}" был заменен на "{{query}}"
    </div>
% end
    <div id="snippets">
      <ul>
% for i in range(len(snippets)):
% s = snippets[i]
        <li>
          <div class="snippet" style="background-color:{{scolors[i % 6]}};" onmouseover="getElementById('prev{{i}}').style.visibility='visible';" onmouseout="getElementById('prev{{i}}').style.visibility='hidden';">
            <a class="title" href="{{s['url']}}">{{!s['title']}}</a>
            <p>{{!s['text']}}</p>
            <a class="address" href="{{s['url']}}">{{s['url']}}</a>
          </div>
          <div style="border: 60px solid transparent; border-left: 60px solid {{scolors[i % 6]}};">
          </div>
        </li>
% end
      </ul>
    </div>
% for i in range(len(snippets)):
    <img src="{{snippets[i]['image']}}" class="preview" id="prev{{i}}">
% end
    <div id="footer">
      Александр Щербаков &amp; Павел Коваленко &copy; 2015
    </div>
  </body>
</html>