/* global person search box toggling */
$("#jstSearchBox .action-btn-showform").click( function(){
        $(".action-theform").removeClass("d-none");
        $(".action-btn-showform").addClass("d-none");
        $("#jstSearchBox input").focus();
        // close the box if blurred
        $("#jstSearchBox NOTinput.combobox").blur( function(){
            setTimeout( function(){
                $(".action-theform").addClass("d-none");
                $(".action-btn-showform").removeClass("d-none");
            },700);
        });
        // actually change the person
        $("#jstSearchBox [name=person_select]").change(function(){
            var p = $(this).val();
            var u;
            if( p ){
                if( typeof redirect === "function" ){
                    redirect( p );
                }else{
                    // attention: we cann not use template processing here,
                    // therefore use this from preprocessed base.html
                    window.location.href = person_edit_url.replace("/0/","/"+p+"/");
                }
            }
        });
});

