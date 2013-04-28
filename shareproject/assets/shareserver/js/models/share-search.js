define([
	'share_collection'
], function (ShareModelCollection) {
	var ShareSearch = Backbone.Model.extend({
        url: '/api/pooch',
		initialize: function(){
            //this.results = new ShareModelCollection();
            //this.results.fetch({dat
            //this.trigger( "search:ready", this );
        }
	});
	return ShareSearch;
});