function load_ellipse_modal(id, cb = null) {
    var modal_container_id = id + '_container';
    var close_modal_id = id + '_close';
    var overlay_close_selector = modal_container_id + " .overlay";

    $(document).on("click", id, function () {
        if(cb) {
            cb(() => open_ellipse_modal(modal_container_id));
        } else {
            open_ellipse_modal(modal_container_id);
        }
    });
    $(document).on("click", close_modal_id, function (e) {
        e.preventDefault();
        close_ellipse_modal(modal_container_id);
    });
    $(document).on("click", overlay_close_selector, function (e) {
        e.preventDefault();
        close_ellipse_modal(modal_container_id);
    });
}

function open_ellipse_modal(modal_container_id) {
    $(modal_container_id).addClass('open');
    var scrollTop = ($('html').scrollTop()) ? $('html').scrollTop() : $('body').scrollTop();
    $('html').addClass('no_scroll').css('top', -scrollTop);
}

function close_ellipse_modal(modal_container_id) {
    var scrollTop = parseInt($('html').css('top'));
    $(modal_container_id).removeClass('open');
    $('html').removeClass('no_scroll').css('top', '');
    $('html,body').scrollTop(-scrollTop);
}
