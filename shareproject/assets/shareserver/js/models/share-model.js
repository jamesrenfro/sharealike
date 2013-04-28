define([
	'backbone'
], function (Backbone) {
	var ShareModel = Backbone.Model.extend({
        urlRoot: '/api/pooch',
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