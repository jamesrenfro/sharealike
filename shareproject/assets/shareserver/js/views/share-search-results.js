define(['share_collection'], function (ShareModelCollection) {
	var ShareSearchResults = Backbone.View.extend({

        initialize: function() {
            this.listenTo(Backbone.Mediator, 'onBrowse', this.onBrowse);
            this.listenTo(Backbone.Mediator, 'onSearch', this.onSearch);
            this.listenTo(Backbone.Mediator, 'results', this.onResults);
        },
        
        onBrowse: function() {
            Backbone.sync('read', this.collection, { success: this.onSuccess });
        },
        
        onResults: function(collection) {
            if (!this.$el.hasClass('active')) {
                $('#main-carousel').carousel('next');
                $('#main-carousel').carousel('pause');
            }
            this.attributes.results = collection;
            this.render();
        },
        
        onSearch: function(query) {
            var data = {};
            if (query != null && query != '')
                data.term = query;
            Backbone.sync('read', this.collection, { data: data, success: this.onSuccess });
        },
        
        onSuccess: function(collection) {
            Backbone.Mediator.trigger('results', collection);
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