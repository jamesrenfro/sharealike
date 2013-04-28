// Configure RequireJS
require.config({
	baseUrl: 'shareserver',
	paths: {
		backbone: '../../lib/backbone-amd/backbone',
		chai : '../../lib/chai/chai',
		jquery: '../../lib/jquery/jquery',
		mocha: '../../lib/mocha/mocha',
        share_collection: '../js/models/share-collection',
        share_collection_test: '../tests/models/share-collection.test',
        share_dialog: '../js/views/share-dialog',
        share_dialog_test: '../tests/views/share-dialog.test',
        share_model: '../js/models/share-model',
        share_model_test: '../tests/models/share-model.test',
        share_results: '../js/views/share-search-results',
        share_results_test:  '../tests/views/share-search-results.test',
		testem: '/testem',
		underscore: '../../lib/underscore-amd/underscore'
	},
    shim: {
    	'backbone':{deps: ['underscore']},
        'bootstrap':{deps: ['jquery']},
        'chai':{deps: ['mocha']},
        'underscore':{deps: []}
    }
});

// Require libraries
require([ 'require', 'chai', 'mocha','testem' ], function(require, chai) {

	// Chai
	assert = chai.assert;
	should = chai.should();
	expect = chai.expect;

	// Mocha
	mocha.setup('bdd');

	// Require base tests before starting
	require([ 
        'share_collection_test',
        'share_dialog_test',
        'share_model_test', 
        'share_results_test', 
    ], function(ShareCollectionTest, ShareDialogTest, ShareModelTest, ShareResultsTest) {
		// Start runner
		mocha.run();
	});

});