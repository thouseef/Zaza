$(document).ready(function(){
    $("div.rateMe").load("rating/");
    $("#commentForm").load("comment/");
    $(".delete").click(function (){
	id=$(this).parent().attr("id");
	query='comment/'+id+"?action=delete";
	$("#"+id).load(query);
    });
    $("div#rated_books").click(function (){
	alert("clicked");
	query='/user/books';
	$("div.right_box").load(query+' .right_box');
    });
    $("input#New").click(function(){
	$("div#right_section").load("/register");
    });
});
  

  function rate(url)
  {
      if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
	  xmlhttp=new XMLHttpRequest();
	  xmlhttp.open("GET",url,false);
	  xmlhttp.send(null);
      }
      else
      {// code for IE6, IE5
	  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	  xmlhttp.open("GET",url,false);
	  // Do not send null for ActiveX
	  xmlhttp.send();
      }
      document.getElementById('rating').innerHTML=xmlhttp.responseText;
  }

  function rateMe(rating){
      id = rating.id;
      url = "rate/"+id;
      rate(url);
  }
