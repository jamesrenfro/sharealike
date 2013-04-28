requirejs.config({
    baseUrl: 'static',
    paths: {
    	backbone: 'lib/backbone-amd/backbone',
    	bootstrap: 'lib/bootstrap/docs/assets/js/bootstrap',
    	handlebars: 'lib/handlebars/handlebars',
    	jquery: 'lib/jquery/jquery',
        share_dialog: 'shareserver/js/views/share-dialog',
        share_model: 'shareserver/js/models/share-model',
        share_collection: 'shareserver/js/models/share-collection',
        share_router: 'shareserver/js/routes/router',
        share_search: 'shareserver/js/models/share-search',
        share_search_form: 'shareserver/js/views/share-search-form',
        share_search_results: 'shareserver/js/views/share-search-results',
        underscore: 'lib/underscore-amd/underscore'
    },
    shim: {
    	'backbone':{deps: ['underscore']},
        'bootstrap':{deps: ['jquery']},
        'underscore':{deps: []}
    }
});

requirejs([
	'share_dialog',
    'share_collection',
    'share_search_form',
    'share_search_results',
    'backbone',
    'bootstrap'
], function (ShareDialog, ShareModelCollection, ShareSearchForm, ShareSearchResults, Backbone, bootstrap) {

    $(function() {
        Backbone.Mediator = {};
        _.extend(Backbone.Mediator, Backbone.Events);
        
        var collection = new ShareModelCollection();
        
        var dialog = new ShareDialog({el: $('#share-dialog')});
        var form = new ShareSearchForm({el: $('#search-form')});
        var results = new ShareSearchResults({el: $('#search-results'), collection: collection});
        Backbone.history.start();
	});

});