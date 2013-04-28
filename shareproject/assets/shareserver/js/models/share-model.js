define([
	'backbone'
], function (Backbone) {
	var ShareModel = Backbone.Model.extend({
		defaults : function() {
			return {
				title : "",
				content : "",
				created: new Date()
			};
		},
	});
	return ShareModel;
});