$(document).ready(function(){
  });

  $(".button-collapse").sideNav();

  $("#btn_add_activity").click(function(){
    $("#frm_add_activity").toggle(); 
  });

  $("#btn_add_bckt").click(function(){
    $("#frm_add_bckt_lst").toggle(); 
  });

  $(".btn_delete").click(function(){
    $("#frm_del_activity").toggle(); 
  });

  $("#edit").click(function(){
    $("#up_title").value = $('#activ_ttl').html
    $('#up_desc').value = $('#activ_desc').html
  });

  $(document).ready(function(){
    $('.modal').modal();
  });

   if ($(".chkbox").prop("checked"))
    $(".chkbox").prop("checked", false);
  else
    $(".chkbox").prop("checked", true);
