$(document).ready(function () {
    $('#footer_android_download_app_nudge').on('click', function () {
        track_ga_event('footer_android_download_app_nudge');
    });

    $('#footer_ios_download_app_nudge').on('click', function () {
        track_ga_event('footer_ios_download_app_nudge');
    });

    $('#similar_internships_download_app_nudge').on('click', function () {
        track_ga_event('similar_internships_download_app_nudge');
    });

    $('#my_applications_download_app_nudge').on('click', function () {
        track_ga_event('my_applications_download_app_nudge');
    });

    $('#todo_list_download_app_nudge').on('click', function () {
        track_ga_event('todo_list_download_app_nudge');
    });

    $('#hamburger_download_app_nudge').on('click', function () {
        track_ga_event('hamburger_download_app_nudge');
    });
});

function track_ga_event(element) {
    if (typeof dataLayer !== 'undefined') {
        dataLayer.push({
            event: 'app_nudge_tracker',
            click: element,
        });
    }
}
