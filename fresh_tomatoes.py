import os
import re
import webbrowser

# Styles and scripting for the page
main_page_head = '''
<head>
	<meta charset="utf-8">
	<title>Fresh Tomatoes!</title>

	<!-- Bootstrap 3 -->
	<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
	<link href="http://fonts.googleapis.com/css?family=Nixie+One" rel="stylesheet" type="text/css">
	<link href="http://fonts.googleapis.com/css?family=Ledger" rel="stylesheet" type="text/css">
	<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
	<script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
	<style type="text/css" media="screen">
		body {
			padding-top: 80px;
		}
		#trailer .modal-dialog {
			margin-top: 200px;
			width: 640px;
			height: 480px;
		}
		.hanging-close {
			position: absolute;
			top: -12px;
			right: -12px;
			z-index: 9001;
		}
		#trailer-video {
			width: 100%;
			height: 100%;
		}
		.scale-media {
			padding-bottom: 56.25%;
			position: relative;
		}
		.scale-media iframe {
			border: none;
			height: 100%;
			position: absolute;
			width: 100%;
			left: 0;
			top: 0;
			background-color: white;
		}

		.view {
			width: 270px;
			height: 340px;
			margin: 30px;
			border: 10px solid #fff;
			overflow: hidden;
			position: relative;
			text-align: center;
			box-shadow: 1px 1px 1px 2px #e6e6e6;
			cursor: default;
		}
		.view .mask {
			width: 220px;
			height: 340px;
			position: absolute;
			overflow: hidden;
			top: 0;
			left: 15px;
			background-color: rgba(232, 232, 232, 0.5);
			transition: all 0.5s linear;
			opacity: 0;
		}
		.view img {
			width: 220px;
			height: 340px;
			display: block;
			position: relative;
			transform: scaleY(1);
			transition: all 0.7s ease-in-out;
		}
		.view h2 {
		  	font: 600 18px/1.2 'Nixie One', Georgia, serif;
			text-align: center;
			position: relative;
			padding: 10px;
			background: rgba(0, 0, 0, 0.8);
			margin: 20px 0 0 0;
			border-bottom: 1px solid rgba(0, 0, 0, 0.3);
			background: transparent;
			margin: 20px 40px 10px 40px;
			transform: scale(0);
			color: #333;
			transition: all 0.5s linear;
			opacity: 0;
		}
		.view p {
		  	font: 400 14px/1.6 'Ledger', Garamond, Georgia, serif;
			position: relative;
			color: #333;
			padding: 10px 20px 20px;
			opacity: 0;
			transform: scale(0);
			transition: all 0.5s linear;
		}
		.view:hover img {
			transform: scale(10);
			opacity: 0;
		}
		.view:hover .mask {
			opacity: 1;
		}
		.view:hover h2, .view:hover p{
			transform: scale(1);
			opacity: 1;
		}
		.navbar {
			background: rgb(232,232,232);
		  	border: none;
		}
		.custom-nav-item {
			font-style: oblique;
			text-transform: uppercase;
			border-bottom: 2px solid rgb(232,232,232);
		}
		.custom-nav-item:hover {
			background: rgb(246,246,246);
			border-bottom: 2px solid rgba(16,16,16,0.5);
			transition: border 0.8s ease;
			transition: background 0.8s ease;
		}
		.navbar-nav {
			display: table;
			margin: 0 auto;
			float: none;
		}
		.navbar-nav a {
			color: rgb(110,110,110);
			font: 600 18px/1.2 'Nixie One', Georgia, serif;
		}
		.non-hover:hover {
			background: rgb(232,232,232) !important;
			cursor: default;
		}
		.smallcaps {
			font-variant: small-caps;
		}
	</style>
	<script type="text/javascript" charset="utf-8">
		// Pause the video when the modal is closed
		$(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
			// Remove the src so the player itself gets removed, as this is the only
			// reliable way to ensure the video stops playing in IE
			$("#trailer-video-container").empty();
		});
		// Start playing the video whenever the trailer modal is opened
		$(document).on('click', '.view', function (event) {
			var trailerYouTubeId = $(this).attr('data-trailer-youtube-id');
			var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
			$("#trailer-video-container").empty().append($("<iframe></iframe>", {
				'id': 'trailer-video',
				'type': 'text-html',
				'src': sourceUrl,
				'frameborder': 0
			}));
		});
		// Animate in the movies when the page loads
		$(document).ready(function () {
			$('.movie-tile').hide().first().show("fast", function showNext() {
				$(this).next("div").show("fast", showNext);
			});
			//Highlight movie tile on hover by adjusting the opacity
			$('.movie-tile').hover(function () {
				$('body').css('background', 'rgba(0, 0, 0, 0.4)');
				$(this).css('background', 'rgba(255, 255, 255, 1)');
			}, function () {
				$('body').css('background', '');
				$(this).css('background', '');
			});

			//Bind click handlers to the navbar
			$('.custom-nav-item a').click(function() {
			   var genre = $(this).text();
			   $('.view').hide();
			   $('.' + genre).show();
			});
		});

	</script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
	<body>
		<!-- Trailer Video Modal -->
		<div class="modal" id="trailer">
			<div class="modal-dialog">
				<div class="modal-content">
					<a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
						<img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
					</a>
					<div class="scale-media" id="trailer-video-container">
					</div>
				</div>
			</div>
		</div>

		<!-- Main Page Content -->
		<div class="container">
			<div class="navbar navbar-fixed-top" role="navigation">

				<div class="container">
				<ul class="nav navbar-nav">
					<li role="presentation" class="custom-nav-item"><a href="#">Scifi</a></li>
					<li><a class="non-hover" href="#">/</a></li>
					<li role="presentation" class="custom-nav-item"><a href="#">Drama</a></li>
					<li><a class="non-hover" href="#">/</a></li>
					<li role="presentation" class="custom-nav-item"><a href="#">Comedy</a></li>
					<li><a class="non-hover" href="#">/</a></li>
					<li role="presentation" class="custom-nav-item"><a href="#">Thriller</a></li>
					<li><a class="non-hover" href="#">/</a></li>
					<li role="presentation" class="custom-nav-item"><a href="#">Noir</a></li>
				</ul>
					</div>
			</div>
		</div>
		<div class="container">

			{movie_tiles}

		</div>
	</body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="{movie_genre} view col-md-4" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
	<img src="{poster_image_url}">
	<div class="mask">
		<h2>{movie_title}</h2>
		<p>{description}</p>
	</div>
</div>
'''

class Movie:
    """
	A class representing a movie object.
	"""

    def __init__(self, data_file):
        self.data_url = 'data/' + data_file
        self.poster_image_url = 'img/%s.jpg' % data_file.split('.')[0]
        self.read_description()

    def read_description(self):
        with open(self.data_url) as fh:
            self.title = fh.readline().rstrip()
            self.genre = fh.readline().rstrip()
            self.trailer_youtube_url = fh.readline().rstrip()
            self.description = fh.read()

my_movies = (
             Movie("interstellar.txt"),
             Movie("mulholland.txt"),
             Movie("darkcity.txt"),
             Movie("believer.txt"),
             Movie("truegrit.txt"),
             Movie("fargo.txt"),
             Movie("rainman.txt"),
             Movie("halfnelson.txt"),
             Movie("fountain.txt"),
             Movie("existenz.txt"),
             Movie("grantorino.txt"),
             Movie("sincity.txt"),
             Movie("crank.txt"),
             Movie("shining.txt"),
             Movie("bluevelvet.txt"),
             Movie("burn.txt"),
             Movie("inception.txt"),
             Movie("tattoo.txt"),
             Movie("clockwork.txt")
             )

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
                                             movie_title=movie.title,
                                             movie_genre=movie.genre,
                                             description=movie.description,
                                             poster_image_url=movie.poster_image_url,
                                             trailer_youtube_id=trailer_youtube_id
                                             )
    return content

def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the placeholder for the movie tiles with the actual dynamically generated content
    rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

if __name__ == "__main__":
    open_movies_page(my_movies)
