function popover_tooltip_light_with_heading(id, heading, content, placement='bottom') {
    var popover_close_id = 'popover_close_' + id.substr(1);
    var title = '<div class="h-12-semi-bold">' + heading +'</div><i class="ic-24-cross" id="' + popover_close_id + '"></i>'
    var popover = $(id).popover({
        placement: placement,
        html: true,
        title : title,
        template: '<div class="popover popover-light popover-custom"><div class="arrow"></div><div class="popover-inner"><div class="popover-header"></div><div class="popover-body"><p></p></div></div></div>',
        content: content,

    });
    $(document).on("click", '#' + popover_close_id, function() {
        $(id).popover('hide');
    });
    return popover;
}

function popover_tooltip_light_without_heading(id, content, placement='bottom') {
    var popover_close_id = 'popover_close_' + id.substr(1);
    var popover = $(id).popover({
        placement: placement,
        html: true,
        template: '<div class="popover popover-light popover-custom noheading"><div class="arrow"></div><div class="popover-inner"><div class="popover-header"></div><div class="popover-body"><p></p></div></div><i class="ic-24-cross" id="' + popover_close_id + '"></i></div>',
        content: content,

    });
    $(document).on("click", '#' + popover_close_id, function() {
        $(id).popover('hide');
    });
    return popover;
}

function popover_tooltip_dark_with_heading(id, heading, content, placement='bottom', trigger='click') {
    var popover_close_id = 'popover_close_' + id.substr(1);
    var title = '<div class="h-12-semi-bold">' + heading +'</div><i class="ic-24-cross" id="' + popover_close_id + '"></i>'
    var popover = $(id).popover({
        placement: placement,
        trigger: trigger,
        html: true,
        title : title,
        template: '<div class="popover popover-dark popover-custom"><div class="arrow"></div><div class="popover-inner"><div class="popover-header"></div><div class="popover-body"><p></p></div></div></div>',
        content: content,

    });
    $(document).on("click", '#' + popover_close_id, function() {
        $(id).popover('hide');
    });
    return popover;
}

function popover_tooltip_dark_without_heading(id, content, placement='bottom') {
    var popover_close_id = 'popover_close_' + id.substr(1);
    var popover = $(id).popover({
        placement: placement,
        html: true,
        template: '<div class="popover popover-dark popover-custom noheading"><div class="arrow"></div><div class="popover-inner"><div class="popover-header"></div><div class="popover-body"><p></p></div></div><i class="ic-24-cross" id="' + popover_close_id + '"></i></div>',
        content: content,

    });
    $(document).on("click", '#' + popover_close_id, function() {
        $(id).popover('hide');
    });
    return popover;
}

function popover_tooltip_light_small(id, content, placement='bottom', position='') {
    var popover = $(id).popover({
        placement: placement,
        html: false,
        sanitize: false,
        template: '<div class="popover popover-small popover-light' + position + '"><div class="arrow"></div><div class="popover-inner"><div class="popover-body"><p></p></div></div></div>',
        content: content,

    });
    return popover;
}
function popover_tooltip_dark_small(id, content, placement='bottom', position='') {
    var popover = $(id).popover({
        placement: placement,
        html: false,
        sanitize: false,
        template: '<div class="popover popover-small popover-dark ' + position +'"><div class="arrow"></div><div class="popover-inner"><div class="popover-body"><p></p></div></div></div>',
        content: content,

    });
    return popover;
}