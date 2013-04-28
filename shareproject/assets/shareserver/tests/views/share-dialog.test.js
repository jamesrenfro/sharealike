define([ 'share_dialog', 'share_router', 'mocha', 'chai' ], function(ShareDialog, ShareRouter, mocha, chai) {

	var should = chai.should();
	describe("ShareDialog", function() {
		beforeEach(function(){
            this.router = new ShareRouter();
            this.dialog = new ShareDialog({el: $('#share-dialog'), attributes: { router : this.router } });
        })
        it("render() should return a model", function() {
            this.dialog.titleInput.val('Test');
            this.dialog.contentInput.val('Another');
            
            var model = this.dialog.render().model;
            model.should.be.an("object");
        });
	});
});