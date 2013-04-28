requirejs.config({
    baseUrl: 'static',
    paths: {
    	backbone: 'lib/backbone-amd/backbone',
    	bootstrap: 'lib/bootstrap/docs/assets/js/bootstrap',
        bootstrap_lightbox: 'lib/bootstrap-lightbox/build/bootstrap-lightbox',
    	handlebars: 'lib/handlebars/handlebars',
    	jquery: 'lib/jquery/jquery',
        share_dialog: 'shareserver/js/views/share-dialog',
        share_model: 'shareserver/js/models/share-model',
        share_collection: 'shareserver/js/models/share-collection',
        share_router: 'shareserver/js/routers/share-router',
        share_search_form: 'shareserver/js/views/share-search-form',
        share_search_results: 'shareserver/js/views/share-search-results',
        underscore: 'lib/underscore-amd/underscore'
    },
    shim: {
    	'backbone':{deps: ['underscore']},
        'bootstrap':{deps: ['jquery']},
        'bootstrap_lightbox':{deps: ['jquery','bootstrap']},
        'handlebars':{exports: 'Handlebars'},
        'underscore':{deps: []}
    }
});

requirejs([
    'share_router',
	'share_dialog',
    'share_collection',
    'share_search_form',
    'share_search_results',
    'backbone',
    'handlebars',
    'bootstrap',
    'bootstrap_lightbox'
], function (ShareRouter, ShareDialog, ShareModelCollection, ShareSearchForm, ShareSearchResults, Backbone, Handlebars, bootstrap, bootstrap_lightbox) {
    
    Backbone.Mediator = {};
    _.extend(Backbone.Mediator, Backbone.Events);
              
    $(function() {
        var router = new ShareRouter();
    
        var collection = new ShareModelCollection();
        var dialog = new ShareDialog({el: $('#share-dialog'), attributes: { router : router } });
        var form = new ShareSearchForm({el: $('#search-form'), attributes: { router : router } });
        
        var resultTemplateSource = $("#search-result-template").html();
        var resultTemplate = Handlebars.compile(resultTemplateSource);
        
        var results = new ShareSearchResults({el: $('#search-results'), collection: collection, attributes: { resultTemplate: resultTemplate } });
        
        
        Backbone.history.start();
	});

});