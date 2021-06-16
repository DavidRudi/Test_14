odoo.define('fal_select_followers.many2manytags', function (require) {
"use strict";

var BasicModel = require('web.BasicModel');
var core = require('web.core');
var form_common = require('web.view_dialogs');
var field_registry = require('web.field_registry');
var relational_fields = require('web.relational_fields');

var M2MTags = relational_fields.FieldMany2ManyTags;
var _t = core._t;

BasicModel.include({

	_setInvalidEmailTagsCompose: function (record, fieldName) {
		var self = this;
        var localID = (record._changes && fieldName in record._changes) ?
                        record._changes[fieldName] :
                        record.data[fieldName];
        var list = this._applyX2ManyOperations(this.localData[localID]);
        var invalidPartnerIds = [];
        _.each(list.data, function (id) {
            var record = self.localData[id];
            if (!record.data.email) {
                invalidPartnerIds.push(record);
            }
        });
        var def;

        if (invalidPartnerIds.length) {
            // remove invalid partners
            var changes = {operation: 'DELETE', ids: _.pluck(invalidPartnerIds, 'id')};
            def = this._applyX2ManyChange(record, fieldName, changes);
        }
        console.log("AAAAAAAAAAAAAAAAAAAAAa");
        console.log(localID);
        console.log(list);

        return Promise.resolve(def).then(function () {
            return {
                invalidPartnerIds: _.pluck(invalidPartnerIds, 'res_id'),
            };
        });
	},
	
});

var SelectedMailTags = M2MTags.extend({
	tag_template: "SelectedMailTags",
    fieldsToFetch: _.extend({}, M2MTags.prototype.fieldsToFetch, {
        email: {type: 'char'},
    }),
    specialData: "_setInvalidEmailTagsCompose",

    _checkEmailPopup: function () {
    	var self = this;

        var popupDefs = [];
        var validPartners = [];

        _.each(this.record.specialData[this.name].invalidPartnerIds, function (resID) {
            var def = new Promise(function (resolve, reject) {
                var pop = new form_common.FormViewDialog(self, {
                    res_model: self.field.relation,
                    res_id: resID,
                    context: self.record.context,
                    title: "",
                    on_saved: function (record) {
                        if (record.data.email) {
                            validPartners.push(record.res_id);
                        }
                    },
                }).open();
                pop.on('closed', self, function () {
                    resolve();
                });
            });
            popupDefs.push(def);
            console.log("BBBBBBBBBBBBBBBBBBBB");
            console.log(def);
            console.log(popupDefs);
        });

        return Promise.all(popupDefs).then(function() {
            // All popups have been processed for the given ids
            // It is now time to set the final value with valid partners ids.
            validPartners = _.uniq(validPartners);
            if (validPartners.length) {
                var values = _.map(validPartners, function (id) {
                    return {id: id};
                });
                self._setValue({
                    operation: 'ADD_M2M',
                    ids: values,
                });
            }
        });
    },

    _render: function () {
        var self = this;
        var _super = this._super.bind(this);
        return new Promise(function (resolve, reject) {
            if (self.record.specialData[self.name].invalidPartnerIds.length) {
                resolve(self._checkEmailPopup());
            } else {
                resolve();
            }
        }).then(function () {
            return _super.apply(self, arguments);
        });
    },
});

field_registry.add('many2many_tags_email', SelectedMailTags);
});
