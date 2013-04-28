define([
	'share_model'
], function (ShareModel) {
	var ShareModelCollection = Backbone.Collection.extend({
        model: ShareModel,
        url: '/api/pooch'
	});
	return ShareModelCollection;
});