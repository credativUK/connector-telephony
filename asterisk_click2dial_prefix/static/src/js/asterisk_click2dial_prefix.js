/* Base phone module for OpenERP
   Copyright (C) 2016 Ondřej Kuzník <ondrej.kuznik@credativ.co.uk>
   The licence is in the file __openerp__.py */

odoo.define('asterisk_click2dial_prefix.click2dial', function (require) {
    var base_phone = require('base_phone.base_phone');
    var web_client = require('web.web_client');
    var core = require('web.core');
    var _t = core._t;

    core.form_widget_registry.get('phone').include({
        init: function() {
            this._super.apply(this, arguments);
        },
        render_value: function() {
            this._super.apply(this, arguments);

            var self = this;
            var phone_num = this.get('value');
            var click2dial_text = '';
            if (this.$el.find('#click2dial').text()
                    && !this.options.dial_button_invisible) {
                click2dial_text = _t('Choose');
            }

            this.$el.find('#click2dial_prefix').off('click');
            this.$el.find('#click2dial_prefix')
                .text(click2dial_text)
                .on('click', function(ev) {
                    ev.preventDefault()
                    var context = {
                        'default_phone_number': phone_num,
                        'default_click2dial_model': self.view.dataset.model,
                        'default_click2dial_id': self.view.datarecord.id
                    };
                    var action = {
                        name: 'Choose prefix',
                        type: 'ir.actions.act_window',
                        res_model: 'asterisk.dialout.prefix.wizard',
                        view_mode: 'form',
                        views: [[false, 'form']],
                        target: 'new',
                        context: context,
                    };
                    web_client.action_manager.do_action(action);
                })
        }
    });
});
