requirejs.config({
    baseUrl: 'static',
    paths: {
    	backbone: 'lib/backbone-amd/backbone',
    	bootstrap: 'lib/bootstrap/docs/assets/js/bootstrap',
    	handlebars: 'lib/handlebars/handlebars',
    	jquery: 'lib/jquery/jquery',
        share_dialog: 'shareserver/js/views/share-dialog',
        share_model: 'shareserver/js/models/share-model',
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
    'bootstrap'
], function (ShareDialog, bootstrap) {

    $(function() {
		var dialog = new ShareDialog({el: $('#share-dialog')});

	});

});