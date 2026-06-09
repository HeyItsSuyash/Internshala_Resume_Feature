$(document).ready(function () {

    function initFooterToggle() {
        var width = $(window).width();

        if (width <= 991) {
            var expandBtn = $('.pre_footer_section .footer_heading');

            expandBtn.off('click');
            expandBtn.on('click', function () {
                var $this = $(this);
                var $section = $this.closest('.pre_footer_section');
                var $footerList = $section.find('.footer_list_component');
                var $icon = $this.find('i');

                if ($footerList.is(':visible')) {
                    $footerList.slideUp(200);
                    $icon.removeClass('ic-24-minus').addClass('ic-24-plus');
                } else {
                    $('.pre_footer_section .footer_list_component').slideUp(200);
                    $('.pre_footer_section .footer_heading i')
                        .removeClass('ic-24-minus')
                        .addClass('ic-24-plus');

                    $footerList.slideDown(200);
                    $icon.removeClass('ic-24-plus').addClass('ic-24-minus');
                }
            });

            $('.pre_footer_section').first().find('.footer_heading').click();

        } else {
            $('.pre_footer_section .footer_list_component').show();
            $('.pre_footer_section .footer_heading i')
                .removeClass('ic-24-minus')
                .addClass('ic-24-plus');

            $('.pre_footer_section .footer_heading').off('click');
        }
    }

    initFooterToggle();

    function renderFooterList(footerList) {
        var $footerContainer = $("#footer-about-us-container-r991 .footer_list");
        $footerContainer.empty();

        footerList.forEach(function (item) {
            if (item.link && item.link.trim() !== "") {
                var $link = $("<a>")
                    .attr("href", item.link)
                    .text(item.key);
                $footerContainer.append($link);
            } else {
                var $text = $("<span>").text(item.key);
                $footerContainer.append($text);
            }
        });
    }

    function handleFooterList() {
        var $footerContainer = $("#footer-about-us-container-r991");

        if ($footerContainer.length === 0) return;

        var width = $(window).width();

        if (width <= 991 && width > 575) {
            renderFooterList(footer_list_r991);
        } else if (width <= 575) {
            renderFooterList(footer_list_r575);
        } else {
            $footerContainer.find(".footer_list").empty();
        }
    }

    handleFooterList();

    $(window).resize(function () {
        handleFooterList();
        initFooterToggle();
    });
});
