$(document).ready(function(){
    $("#a").click(function(){
	$("#commentForm").load("comment/");
	$("#a").hide();
    });
    $(".submit").click(function(){
	$("#a").show();
    });
    $(".delete").click(function (){
	alert("clicked delete");
	id=$(this).parent().attr("id");
	query='comment/'+id+"?action=delete";
	$("#"+id).load(query);
    });

});
