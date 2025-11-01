/*!
 * jTruncate - jQuery Plugin
 * version: 0.8.1
 * @requires jQuery v1.7 or later
 *
 * Copyright 2015 Fernando Miranda - fernando@projeteweb.com.br
 *
 */

(function ($) {
    $.fn.truncate = function(options) {

        var settings = $.extend({
            length: 50,
            limit: -1,
            style: 'bootstrapPopover',
            trigger: 'hover', // hover | click
            trailing: '...',
            placement: 'auto' // top | bottom | left | right | auto
        }, options);

        return this.each(function() {
        	var that = $(this),
        		text = $.trim(that.text()),
        		length = text.length;

        	if (length > settings.length) {
        		var arr = text.split('', settings.length),
        			textTruncated = arr.join('') + settings.trailing;

        		if (settings.limit > -1) {
        			text = text.split('', settings.limit).join('');
        		}

        		that.addClass('text-truncated').text(textTruncated).data('text-original', text);

        		switch (settings.style) {
        		case 'bootstrapPopover':
        			$(that).popover({
        				trigger: settings.trigger,
        				content: text,
        				placement: settings.placement
        			}).on('shown.bs.popover', function() {
        				that.addClass('truncate-full-open');
        			}).on('hidden.bs.popover', function () {
        				that.removeClass('truncate-full-open');
        			});
        			break;
        		default:
        			break;
        		}
        	}
        });

    };
}(jQuery));
