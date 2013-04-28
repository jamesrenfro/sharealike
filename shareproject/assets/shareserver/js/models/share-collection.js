define([
	'share_model'
], function (ShareModel) {
	var ShareModelCollection = Backbone.Collection.extend({
        events: {
//            'reset': 'onReset',
//            'sync': 'onSync'
        },
        model: ShareModel,
        url: '/api/pooch',
        defaults : function() {
			return {
				search_term : ""
			};
		},
        onReset: function() {
            alert('Reset!');
        },
        onSync: function(model, resp, options) {
            alert('Heya!');
        }
	});
	return ShareModelCollection;
});