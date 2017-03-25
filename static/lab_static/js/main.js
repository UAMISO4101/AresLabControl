jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.open($(this).data("href"),'_blank');
    });
});