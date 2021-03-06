define(['backbone'], function (Backbone) {
	var ShareSearchForm = Backbone.View.extend({

		events: {
			'submit': 'onSubmit'
		},
        
        initialize: function() {
            this.listenTo(Backbone.Mediator, 'onSearch', this.onSearch);
        },
        
        onSearch: function(query) {
            this.$el.find(':input[type="text"]').val(query);
        },
        
        onSubmit: function(event) {
            var term = $(event.currentTarget).find(":input").val();
            var fragment = 'search';
            if (term != null && term != '') {
                fragment += '/' + term;
                this.attributes.router.navigate(fragment, {trigger: true});
            } else {
                this.attributes.router.navigate('blank', {trigger:true});
            }
            return false;
        },
                
    });
    
    return ShareSearchForm;
});