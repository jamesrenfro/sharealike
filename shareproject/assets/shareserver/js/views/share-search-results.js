define(['share_collection'], function (ShareModelCollection) {
	var ShareSearchResults = Backbone.View.extend({

		events: {
        
		},
        
        initialize: function() {
            this.listenTo(Backbone.Mediator, 'browse', this.onBrowse);
            this.listenTo(Backbone.Mediator, 'search', this.onSearch);
        },
        
        onBrowse: function() {
            this.doShow();
            Backbone.sync('read', this.collection, { success: this.onSuccess });
            //this.$el.load("/browse");
        },
        
        onSearch: function(query) {
            this.doShow();
            this.$el.load("/search?term=" + query);
        },
        
        onSuccess: function(event) {
            this.render();
        },
        
        doShow: function() {
            if (!this.$el.hasClass('active')) {
                $('#main-carousel').carousel('next');
                $('#main-carousel').carousel('pause');
            }
        },
        
        render: function() {
            var html = '';
            html += '<div class="container"><br/><ul>';
            $.each(this.collection, function(i, model) {
                html += '<li>' + model.dog_name + '</li>';
            });
            html += '</ul></div>';
            this.$el.html(html);
        }
        
    });
    
    return ShareSearchResults;
});