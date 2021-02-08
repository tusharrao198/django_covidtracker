$(function () {
    // Back to top button
    $('.back-to-top').on('click', function() {
        $('html, body').animate({
            scrollTop: 0
        }, 1000, 'easeInOutExpo');
        return false;
    });

    $('.darkMode').on('click', function() {
        if (!$('#introduction').hasClass('bg-dark')) {
            $('#introduction').removeClass("bg-light");
            $('#introduction').addClass("bg-dark");
        }
        else if (!$('#introduction').hasClass('bg-light')) {
            $('#introduction').removeClass("bg-dark");
            $('#introduction').addClass("bg-light");
        }
    });

    // navbar-toggler button
    $('.toggle-button').on('click', function () {
        $('.animated-icon').toggleClass('open');
    });

    /*--/ Navbar Menu Reduce /--*/
    $(window).trigger("scroll");
    $(window).on("scroll", function() {
        const pixels = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
        if ($(window).scrollTop() > pixels) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
});(jQuery);