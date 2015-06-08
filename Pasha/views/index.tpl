<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{query}} | Diogenes</title>
    <link href="/static/styles.css" rel="stylesheet">
    <!--<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">-->
  </head>
  <body class="content_area">
    <!--<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container-fluid">
        <div class="navbar-header">
          
          <a class="navbar-brand" href="#">Logo</a>
          <form class="navbar-form navbar-left">
              <input type="text" class="form-control" placeholder="Search...">
            </form>
        </div>
      </div>
    </div>-->
    <div id="menu">
      <img src="" id="logo">
      <form>
        <input type="text" value="{{query}}" name="query">
        <button>Search <img src="" id="search"></button>
      </form>
    </div>
    <div id="snippets">
      <ul>
% i = 0
% for s in snippets: 
  <li>
  <div class="snippet" style="background-color:{{scolors[i % 6]}};">
  <a class="title" href="{{s['url']}}">{{!s['title']}}</a>
  <p>... {{!s['text']}} ...</p>
  <a class="address" href="{{s['url']}}">{{s['url']}}</a>
  </div>
  <div style="border: 50px solid transparent; border-left: 50px solid {{scolors[i % 6]}};">
  </div>
  </li>
% i += 1  
% end

  </body>
</html>