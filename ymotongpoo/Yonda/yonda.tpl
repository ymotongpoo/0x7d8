<!-- -*- mode: html; coding:utf-8 -*- -->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
 "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns:py="http://genshi.edgewall.org/"
	  lang="ja">
  <head>
	<meta name="author" content="ymotongpoo -- http://d.hatena.ne.jp/ymotongpoo/"/>
	<link rel="stylesheet" href="style.css" type="text/css" media="screen"/>
	<title>よんだ？</title>
  </head>
  <body>
	<div class="ranking">
	  <h3>人気「あとでよむ」エントリ</h3>
	  <ol>
		<li py:for="bookmark in bookmarks">
		<a href="${bookmark.url}">${bookmark.title}<img src="http://b.hatena.ne.jp/entry/image/normal/${bookmark.url}"/></a>
		</li>
	  </ol>
	</div>

	<div class="ranking">
	  <h3>ホット「あとでよむ」エントリ</h3>
	  <ol>
		<li py:for="bookmark in hotentry">
		<a href="${bookmark.url}">${bookmark.title}<img src="http://b.hatena.ne.jp/entry/image/normal/${bookmark.url}"/></a>
		</li>
	  </ol>
	</div>
	
	<!-- Google Analytics -->
	<script type="text/javascript">
	  var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
	  document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
	</script>
	<script type="text/javascript">
	  try {
	  var pageTracker = _gat._getTracker("UA-6420772-2");
	  pageTracker._trackPageview();
	  } catch(err) {}
	</script>
  </body>
</html>
