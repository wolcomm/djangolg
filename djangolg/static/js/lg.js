$(document).ready(function () {
    $("#accept-terms-form").submit(function (event) {
        event.preventDefault();
        var query = $(this).serialize();
        $.getJSON("/enter/?", query, function (json) {
            $("[name$='auth_key']").val(json.key);
            $("#accept-terms-modal").modal('hide');
        }).fail(function () {
            $("#accept-terms-checkbox").popover('show');
        })
    });
    $("#accept-terms-modal").modal({
        backdrop: 'static',
        keyboard: false,
    });
    $("#router-select").change(function () {
        var router = $(this).val();
        $("[name='router']").val(router);
    });
    $("[data-toggle='tooltip']").tooltip();
    $("form.lg-control").each(function () {
        $(this).submit(function (event) {
            event.preventDefault();
            var progress = $("#progress")
                .show(0);
            var bar = $("#progress-bar")
                .attr("sytle", "width:10%");
            $("#raw-output-tab-link").tab('show');
            var alert = $("#error-alert")
                .hide("fast");
            var raw = $("#raw-output")
                .text("Please wait...");
            var formatted = $("#formatted-output")
                .text("Please wait...");
            bar.attr("style", "width:20%");
            var query = $(this).serialize();
            bar.attr("style", "width:40%");
            var req = $.getJSON("/lg/?", query);
            req.done(function (json) {
                bar.attr("style", "width:80%");
                raw.text(json.raw);
                formatted.text("Formatted output not supported for this query");
                bar.attr("style", "width:100%");
                progress.hide("slow");
                bar.attr("style", "width:0%");
            });
            req.fail(function (resp) {
                bar.attr("style", "width:80%");
                var msg = " " + resp.statusText + ". Please try again.";
                $("#alert-text").text(msg);
                raw.text("An error occurred");
                formatted.text("An error occurred");
                alert.show("slow");
                bar.attr("style", "width:100%");
                progress.hide("slow");
                bar.attr("style", "width:0%");
            });
        })
    })
    var copy = new Clipboard("#copy-button");
});
