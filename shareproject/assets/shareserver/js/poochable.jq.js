// Pure JQuery
$(document).ready(
		function() {
			var app = {};
			app.clear_modal = function() {
				var $dialog = $('#add-picture-dialog');
				$dialog.find('.control-group').removeClass('error');
				$dialog.find('.help-inline').remove();
				$dialog.find('form')[0].reset();
				$dialog.find(':input').disabled=false;
			};
			app.bad_request = function(jqXHR, textStatus, errorThrown) {
				var modal = $('#add-picture-dialog');
				var errors = $.parseJSON(jqXHR.responseText);

				for ( var key in errors) {
					var selector = '[name="' + key + '"]';
					var error = errors[key][0];
					var el = modal.find(selector);
					el.after('<span class="help-inline">' + error + '</span>');
					el.closest('.control-group').addClass('error');
				}
			};
			app.browse = function() {
				var $search_results = $('#search-results');
				$search_results.load("/browse");
				app.show_results($search_results);
			};
			app.failure = function(jqXHR, textStatus, errorThrown) {
				var source = $("#add-picture-dialog-alert-template").html();
				var template = Handlebars.compile(source);
				var $notification = $("#picture-dialog-notification");
				$notification.html(template({}));
			};
			app.search = function() {
				var data = $('#search-form').serialize();
				var $search_results = $('#search-results');
				$search_results.load("/search", data);
				app.show_results($search_results);
			};
			app.show_results = function($search_results) {
				if (!$search_results.hasClass('active')) {
					$('#main-carousel').carousel('next');
					$('#main-carousel').carousel('pause');
				}
			};
			app.success = function() {
				app.browse();
				$('#add-picture-dialog').modal('hide');
			};

			$('#add-picture-dialog').on('hidden', app.clear_modal);

			$('#browse-button').click(function() {
				app.browse();
			});
			
			$('#search-button').click(function() {
				app.search();
			});
			
			$('#search-form').submit(function() {
				return false;
			});

			$('#upload-button').click(function() {
				var modal = $('#add-picture-dialog');
				var data = new FormData();
				jQuery.each(modal.find('.attachment')[0].files, function(i, file) {
					data.append('attachment', file);
				});
				jQuery.each(modal.find(':input'), function(i, input) {
					var $input = $(input);
					$input.disabled = true;
					var name = $input.attr('name');
					var value = $input.val();
					data.append(name, value);
				});

				app.clear_modal();
				$.ajax({
					url : '/api/pooch',
					data : data,
					processData : false,
					contentType : false,
					type : 'POST',
					statusCode : {
						200 : app.success,
						400 : app.bad_request,
						500 : app.failure,
					}
				});

			});

			// Extending bootstrap-lightbox to load the href data
			$(document).unbind('click.lightbox.data-api');
			$(document).on(
					'click.lightbox.data-api',
					'[data-toggle="lightbox"]',
					function(e) {
						var $this = $(this);
						var href = $this.attr('href');
						var $target = $($this.attr('data-target')
								|| (href && href.replace(/.*(?=#[^\s]+$)/, ''))); // strip
						// for
						// ie7
						var option = $target.data('lightbox') ? 'toggle' : $.extend({
							remote : !/#/.test(href) && href
						}, $target.data(), $this.data());
						var img = $this.attr('data-image') || false;
						var $imgElem;

						e.preventDefault();

						$target.find('.lightbox-content').load(
								href,
								function() {

									if (img) {
										$target.data('original-content', $target.find(
												'.lightbox-content').html());
										$target.find('.lightbox-content').html(
												'<img border="0" src="' + img + '" />');
									}

									$target.lightbox(option).one('hide', function() {
										$this.focus()
									}).one(
											'hidden',
											function() {
												if (img) {
													$target.find('.lightbox-content').html(
															$target.data('original-content'));
													img = undefined;
												}
											});
								});
					});
});