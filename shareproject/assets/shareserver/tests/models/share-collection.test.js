define([ 'share_collection', 'mocha', 'chai' ], function(ShareModelCollection, mocha, chai) {

	var should = chai.should();
	describe("ShareModelCollection", function() {
		it("has model and url", function() {
			var collection = new ShareModelCollection();
            should.exist(collection);
            collection.should.be.an('object');
            
            var model = collection.model;
			should.exist(model);
			model.should.be.an('function');

			var url = collection.url;
			url.should.be.a("string");
			url.should.not.equal("");
		})
	});
});