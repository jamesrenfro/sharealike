define(['share_search'], function (ShareSearch) {
	var ShareSearchForm = Backbone.View.extend({

		events: {
            'click .browse': 'onBrowse',
			'submit': 'onSubmit'
		},
        
        onBrowse: function(event) {
            Backbone.Mediator.trigger('browse');
        },
        
        onSubmit: function(event) {
            var term = $(event.currentTarget).find(":input").val();
            Backbone.Mediator.trigger('search', term);
            return false;
        },
        
        render: function() {
			return this;
		},

		shown: function() {
			this.render();
		},
        
    });
    
    return ShareSearchForm;
});