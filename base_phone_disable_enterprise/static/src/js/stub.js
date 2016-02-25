odoo.define('crm.voip', function(require) {

var core = require('web.core');
var stub = function (parent, action) {
    return { type: 'ir.actions.act_window_close' };
}

core.action_registry.add("reload_panel", stub);
core.action_registry.add("transfer_call", stub);

});
