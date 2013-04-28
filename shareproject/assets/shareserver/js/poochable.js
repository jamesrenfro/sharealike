$(function(){
	var Result = Backbone.Model.extend({
		defaults : function() {
			return {
				dog_name : "",
				url : ""
			};
		},
	});

	var Results = Backbone.Collection.extend({
		model : Result
	});

	var Search = Backbone.Model.extend({
		url : "/api/pooch",

		initialize : function() {
			this.results = new Results(this.get("results"));
			this.trigger("search:ready", this);
		}
	});

	var SearchView = Backbone.View.extend({
						
		events : {
			"click" : "onSubmit",
			"submit form" : "onSubmit"
		},
		
		initialize: function(){
		    this.render();
		},

		onSubmit : function() {
			var search = new Search({
				term : this.$el.find("search-field").val(),
			});

			// You can listen to the "search:ready" event
			search.on("search:ready", this.renderResults, this)

			// this is when a POST request is sent to the server
			// to the URL `/search` with all the search
			// information packaged
			search.save();
			
//			// Make sure that the form doesn't really get submitted to the server
			return false;
		},

		renderResults : function(search) {
			var source = $("#search-result-template").html();
			var template = Handlebars.compile(source);
			var $results = $el.find('search-results');
			$results.append('<ul class="thumbnails">');
			$.each(search.results, function(i, result) {
				var html = template(result);
				$results.append(html);
			});
			$results.append('</ul>');
			
			// TODO: Move this to the Router when "search:ready"
			if (!$results.hasClass('active')) {
				$('#main-carousel').carousel('next');
				$('#main-carousel').carousel('pause');
			}
		}
	});
	
	searchView = new SearchView({el: $("#search-form")});
});

