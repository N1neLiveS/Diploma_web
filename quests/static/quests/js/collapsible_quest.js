$(document).ready(function() {
    $(".collapsible_quest").each(function(index) {
        $(this).on("click", function() {
            $(this).toggleClass("active");
            var content = $(this).next();
            if (content.css("max-height") != "0px") {
                content.css("max-height", "0");
            } else {
                content.css("max-height", content.prop("scrollHeight") + "px");
            }
        });
    });
});