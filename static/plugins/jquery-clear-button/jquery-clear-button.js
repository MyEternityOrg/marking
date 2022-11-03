(function ($) {
    $.fn.jQueryClearButton = function (options) {
        if (!this.is(':visible')) {
            return this;
        }
        let obj = this;
        let obj_id = obj.attr('id');
        let btn_class_name = 'input-clear-' + obj_id;

        let defaults = {
            'always': false,
            'zindex': 0,
            'offset_right': 10,
            'button_width': 20,
            'button_height': 20,
            'color': '#aaa'
        };
        let setting = $.extend(defaults, options); //merge

        $('body').append('<style> input::-ms-clear { visibility:hidden; } </style>');

        let btn_parent = $('<div style="position:relative; margin:0; padding:0; border:none;">');
        this.before(btn_parent);
        this.prependTo(btn_parent);

        let btn = $('<div class="bi bi-x ' + btn_class_name + '"></div>');
        this.before(btn);

        btn.css({
            'position': 'absolute',
            'display': 'none',
            'cursor': 'pointer',
            'z-index': setting.zindex,
            'width': setting.button_width + 'px',
            'height': setting.button_height + 'px',
            'color': setting.color
        });

        let btn_parent_height = btn_parent.height();
        if (!btn_parent_height) {
            btn_parent_height = obj.height();
        }

        let offset_top = (btn_parent_height / 2) - (setting.button_height / 2);
        btn.css({
            'top': offset_top + 'px',
            'right': setting.offset_right + 'px'
        });

        btn.on('click', function () {
            obj.val('').focus();
            if (!setting.always) {
                btn.hide();
            }
        });
        obj.on('input', function () {
            if (obj.val()) {
                btn.show();
            } else {
                if (!setting.always) {
                    btn.hide();
                }
            }
        });

        if (setting.always) {
            btn.show();
        } else {
            obj.on('focus', function () {
                if (obj.val()) {
                    btn.show();
                } else {
                    btn.hide();
                }
            });
            obj.on('blur', function () {
                setTimeout('$(\'.' + btn_class_name + '\').hide()', 200);
            });
            obj.on('mouseover', function () {
                if (obj.val()) {
                    btn.show();
                } else {
                    btn.hide();
                }
            });

        }
        return (this);
    };
})(jQuery);
