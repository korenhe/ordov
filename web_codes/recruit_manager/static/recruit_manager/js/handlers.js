$(document).ready(function () {
    // All sides
    var sides = ["left", "top", "right", "bottom"];
    $("h1 span.version").text($.fn.sidebar.version);

    // Initialize sidebar2s
    for (var i = 0; i < sides.length; ++i) {
        var cSide = sides[i];
        $(".sidebar2." + cSide).sidebar({side: cSide});
    }

    // Click handlers
    $(".btn[data-action]").on("click", function () {
        var $this = $(this);
        var action = $this.attr("data-action");
        var side = $this.attr("data-side");
        console.log("button data-action: ")
        console.log(".sidebar2."+side)
        console.log("sidebar2:"+action)
        $(".sidebar2." + side).trigger("sidebar:" + action);
        return false;
    });
});
