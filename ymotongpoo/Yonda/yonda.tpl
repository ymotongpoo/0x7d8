<!-- -*- mode: html; coding:utf-8 -*- -->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
 "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns:py="http://genshi.edgewall.org/"
	  lang="ja">
  <head>
	<meta name="author" content="ymotongpoo -- http://d.hatena.ne.jp/ymotongpoo/"/>
	<link rel="stylesheet" href="style.css" type="text/css" media="screen"/>
	<title>よんで！</title>
  </head>
  <body>
	<div class="ranking">
	  <h3>総合ランキング</h3>
	  <ol>
		<li py:for="bookmark in bookmarks">
		<a href="${bookmark.url}">${bookmark.title}<img src="http://b.hatena.ne.jp/entry/image/normal/${bookmark.url}"/></a>
		</li>
	  </ol>
	</div>
  </body>
</html>
