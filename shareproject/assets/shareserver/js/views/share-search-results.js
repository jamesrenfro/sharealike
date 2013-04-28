define(['share_collection'], function (ShareModelCollection) {
	var ShareSearchResults = Backbone.View.extend({

        initialize: function() {
            this.listenTo(Backbone.Mediator, 'onBlank', this.onBlank);
            this.listenTo(Backbone.Mediator, 'onBrowse', this.onBrowse);
            this.listenTo(Backbone.Mediator, 'onSearch', this.onSearch);
            this.listenTo(Backbone.Mediator, 'results', this.onResults);
        },
        
        onBlank: function() {
            this.attributes.results = [];
            this.render();
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
            var resultTemplate = this.attributes.resultTemplate;
            var results = { 'results' : this.attributes.results };
            this.$el.html(resultTemplate(results));
        }
        
    });
    
    return ShareSearchResults;
});