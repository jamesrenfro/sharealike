define([
	'backbone'
], function (Backbone) {
    var ShareRouter = Backbone.Router.extend({
        routes: {
            "blank":                "blank",   // #blank
            "browse":               "browse",  // #browse
            "search/:query":        "search",  // #search/joe
            "search/:query/p:page": "search"   // #search/joe/p7
        },
        
        blank: function() {
            Backbone.Mediator.trigger('onBlank');
        },

        browse: function() {
            Backbone.Mediator.trigger('onBrowse');
        },

        search: function(query, page) {
            Backbone.Mediator.trigger('onSearch', query);
        }

    });
    return ShareRouter;
});