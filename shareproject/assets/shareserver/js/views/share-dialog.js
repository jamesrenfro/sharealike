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

            // It would be nice to be able to use this, but currently Backbone doesn't handle multipart on sync
            // There are a bunch of interesting solutions out there, such as this one https://gist.github.com/unixcharles/1278188
            // but assuming that we have HTML5, it seems easier to use the JQuery code in 'upload'
            // Backbone.sync('create', this.model);
            this.upload(this.model);
		},
        
        initialize: function() {
            this.titleInput = this.$('#share-title');
			this.contentInput = this.$('#share-content');
            this.attachmentInput = this.$('#share-attachment');
        },
        
        onComplete: function() {
            // Hide the dialog
			$('#share-dialog').modal('hide');
            //this.attributes.router.navigate('browse', {trigger: true});
			Backbone.Mediator.trigger('onBrowse');
        },
        
        onFailure: function(jqXHR, textStatus, errorThrown) {
            alert(textStatus);
        },
        
        onInvalid: function(jqXHR, textStatus, errorThrown) {
            var errors = $.parseJSON(jqXHR.responseText);

            for ( var key in errors) {
                var selector = '[name="' + key + '"]';
                var error = errors[key][0];
                var $input = $(selector);
                $input.after('<span class="help-inline">' + error + '</span>');
                $input.closest('.control-group').addClass('error');
            }
        },

		render: function() {
			this.model = new ShareModel();
			
			this.titleInput.val('');
			this.contentInput.val('');
            this.attachmentInput.val('');
            
			return this;
		},

		shown: function() {
			this.render();
		},
        
        upload: function(model) {
            var data = new FormData();
			if (model.title != null)
                data.append('share_title', model.title);
            if (model.content != null)
                data.append('share_content', model.content);
            if (model.attachment != null)
                data.append('share_attachment', model.attachment);
            
			$.ajax({
                url : '/api/share',
                data : data,
                processData : false,
                contentType : false,
                type : 'POST',
                statusCode : {
                    200 : this.onComplete,
                    400 : this.onInvalid,
                    500 : this.onFailure,
                }
            });
        }


	});
	return ShareDialog;
});