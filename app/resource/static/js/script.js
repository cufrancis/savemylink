var error = function(msg){
    // alert(msg)
    $("#message-alert").append('<div class="alert alert-danger alert-dismissible fade in" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button><h4>Oh snap! You got an error!</h4><p>'+msg+'</p></div>')
}
