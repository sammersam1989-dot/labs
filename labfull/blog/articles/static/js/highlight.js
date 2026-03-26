$(document).ready(function () {
    // затемнение постов
    $('.one-post').each(function () {
        var $post = $(this);
        var $shadow = $post.find('.one-post-shadow');
        if ($shadow.length === 0) {
            return;
        }

        $shadow.css({
            transition: 'opacity 0.3s ease',
            opacity: 0
        });

        $post.on('mouseenter', function () {
            $shadow.stop(true).animate({ opacity: 0.5 }, 300);
        });

        $post.on('mouseleave', function () {
            $shadow.stop(true).animate({ opacity: 0 }, 300);
        });
    });

    // увеличение логотипа
    $('.logo').hover(
        function () {
            var $img = $(this);
            var origWidth = $img.data('orig-width');
            var origHeight = $img.data('orig-height');

            if (!origWidth || !origHeight) {
                origWidth = $img.width();
                origHeight = $img.height();
                $img.data('orig-width', origWidth);
                $img.data('orig-height', origHeight);
            }

            var newWidth = origWidth + 20;
            var newHeight = origHeight * (newWidth / origWidth);

            $img.stop(true).animate({
                width: newWidth,
                height: newHeight
            }, 200);
        },
        function () {
            var $img = $(this);
            var origWidth = $img.data('orig-width');
            var origHeight = $img.data('orig-height');

            if (origWidth && origHeight) {
                $img.stop(true).animate({
                    width: origWidth,
                    height: origHeight
                }, 200);
            }
        }
    );
});