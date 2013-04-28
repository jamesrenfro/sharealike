// Configure RequireJS
require.config({
	baseUrl: 'shareserver',
	paths: {
		backbone: '../../lib/backbone-amd/backbone',
		chai : '../../lib/chai/chai',
		jquery: '../../lib/jquery/jquery',
		mocha: '../../lib/mocha/mocha',
        share_model: '../js/models/share-model',
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
require([ 'require', 'chai', 'testem', 'mocha' ], function(require, chai) {

	// Chai
	assert = chai.assert;
	should = chai.should();
	expect = chai.expect;

	// Mocha
	mocha.setup('bdd');

	// Require base tests before starting
	require([ '../js/tests/share-model.test' ], function(ShareModelTest) {
		// Start runner
		mocha.run();
	});

});