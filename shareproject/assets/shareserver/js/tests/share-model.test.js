define([ 'share_model', 'mocha', 'chai' ], function(ShareModel, mocha, chai) {

	var should = chai.should();
	describe("ShareModel", function() {
		it("has correct default attributes", function() {
			var model = new ShareModel();
			should.exist(model);
			model.should.be.an('object');

			var title = model.get('title');
			title.should.be.a("string");
			title.should.equal("");
            
            var content = model.get('content');
			content.should.be.a("string");
			content.should.equal("");
            
            var created = model.get('created');
			created.should.be.a("date");
		})
	});
});