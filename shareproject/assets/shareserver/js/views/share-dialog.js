define(['share_model'], function (ShareModel) {
	var ShareDialog = Backbone.View.extend({

		events: {
			'click .btn-primary': 'accept',
			'shown': 'shown'
		},

		accept: function() {
			this.model.title = this.titleInput.val();
			this.model.content = this.contentInput.val();
            this.model.attachment = this.attachmentInput[0].files[0];
			this.created = new Date();

			// Add the new process to the list on the left
			// this.app.add(this.model);

            Backbone.sync('create', this.model);

			// Hide the dialog
			this.$el.modal('hide');
		},

		render: function() {
			this.model = new ShareModel();
			this.titleInput = this.$('#share-title');
			this.contentInput = this.$('#share-content');
            this.attachmentInput = this.$('#share-attachment');
            
			this.titleInput.val('');
			this.contentInput.val('');
            this.attachmentInput.val('');
            
			return this;
		},

		shown: function() {
			this.render();
		}

	});
	return ShareDialog;
});