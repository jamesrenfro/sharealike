define(['share_collection'], function (ShareModelCollection) {
	var ShareSearchResults = Backbone.View.extend({

		events: {
        
		},
        
        initialize: function() {
            this.listenTo(Backbone.Mediator, 'onBrowse', this.onBrowse);
            this.listenTo(Backbone.Mediator, 'onSearch', this.onSearch);
            this.listenTo(Backbone.Mediator, 'results', this.onResults);
        },
        
        onBrowse: function() {
            //this.doShow();
            Backbone.sync('read', this.collection, { success: this.onSuccess });
        },
        
        onResults: function(collection) {
            this.doShow();
            this.attributes.results = collection;
            this.render();
        },
        
        onSearch: function(query) {
            //this.doShow();
            Backbone.sync('read', this.collection, { data: { term: query }, success: this.onSuccess });
            //this.$el.load("/search?term=" + query);
        },
        
        onSuccess: function(collection) {
            Backbone.Mediator.trigger('results', collection);
        },
        
        doShow: function() {
            if (!this.$el.hasClass('active')) {
                $('#main-carousel').carousel('next');
                $('#main-carousel').carousel('pause');
            }
        },
        
        render: function() {
            var $thumbnails = this.$el.find('ul.thumbnails');
            $thumbnails.empty();
            var resultTemplate = this.attributes.resultTemplate;
            $.each(this.attributes.results, function(i, model) {
                $thumbnails.append(resultTemplate(model));
            });
        }
        
    });
    
    return ShareSearchResults;
});