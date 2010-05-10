/*
 * jQuery panelgallery plugin
 * @author admin@catchmyfame.com - http://www.catchmyfame.com
 * @version 1.0
 * @date April 29, 2009
 * @category jQuery plugin
 * @copyright (c) 2009 admin@catchmyfame.com (www.catchmyfame.com)
 * @license CC Attribution-No Derivative Works 3.0 - http://creativecommons.org/licenses/by-nd/3.0/
 */

(function($){
	$.fn.extend({ 
		panelGallery: function(options)
		{
			var defaults = 
			{
				sections : 3,
				imageTransitionDelay : 3000,
				sectionTransitionDelay : 700,
				startDelay : 2000,
				repeat : true,
				direction : "lr"
			};
		var options = $.extend(defaults, options);
	
    		return this.each(function() {
				var o=options;
				var obj = $(this);

				// Preload images
				$("img", obj).each(function(i) { // preload images
					preload = new Image($(this).attr("width"),$(this).attr("height")); 
					preload.src = $(this).attr("src");
				});

				function getRandom()
				{
					return Math.round(Math.random()*100000000);
				}

				var imgArray = $("img", obj);
				$("img:not(:first)", obj).hide(); // Hides all images in the container except the first one
				$("img", obj).css({'position':'absolute','top':'0px','left':'0px'}); // Set the position of all images in the container

				var imgWidth = $("img:first", obj).attr("width"); // Get width of base image;
				var imgHeight = $("img:first", obj).attr("height"); // Get height of base image;
				var sectionWidth = Math.floor(imgWidth/o.sections); // Used when transitioning lr and rl
				var sectionHeight = Math.floor(imgHeight/o.sections); // Used when transitioning tb and bt
				if ((o.direction=="lr" || o.direction=="rl") && imgWidth%o.sections != 0) o.sections++; // This will either equal sections or sections+1
				if ((o.direction=="tb" || o.direction=="bt") && imgHeight%o.sections != 0) o.sections++; // This will either equal sections or sections+1
				$(this).height(imgHeight).width(imgWidth); // Sets the container width and height to match the first image's dimensions

				var imgOffset = 0;
				var panelIDArray = new Array(); // In order to accommodate multiple containers, we need unique div IDs

				if(o.direction == "lr" || o.direction == "rl")
				{
					for(var i=0;i<o.sections;i++)
					{
						panelID = getRandom();
						$(this).append('<div class="section" id="p'+panelID+'">'); // Create a new div 'part'
						$("#p"+panelID).css({'left':imgOffset+'px','background-position':-imgOffset+'px 50%','display':'none'}); // Set the left offset and background position. THIS ISNT WORKING IN WEBKIT
						imgOffset = imgOffset + sectionWidth;	// Increment the offset
						panelIDArray[i] = panelID;
					}
					$("div.section", obj).css({'top':'0px','background-repeat':'no-repeat','position':'absolute','z-index':'10','width':sectionWidth+'px','height':imgHeight+'px','float':'left','background-image':'url('+$("img:eq(1)", obj).attr("src")+')'});
				}

				if(o.direction == "tb" || o.direction == "bt")
				{
					for(var i=0;i<o.sections;i++)
					{
						panelID = getRandom();
						$(this).append('<div class="section" id="p'+panelID+'">'); // Create a new div 'part'
						$("#p"+panelID).css({'top':imgOffset+'px','background-position':'50% '+-imgOffset+'px','display':'none'}); // Set the left offset and background position
						imgOffset = imgOffset + sectionHeight;	// Increment the offset
						panelIDArray[i] = panelID;
					}
					$("div.section", obj).css({'left':'0px','background-repeat':'no-repeat','position':'absolute','z-index':'10','width':imgWidth+'px','height':sectionHeight+'px','background-image':'url('+$("img:eq(1)", obj).attr("src")+')'});
				}

				if (o.direction == "rl" || o.direction == "bt") panelIDArray.reverse();

				var doingSection=0;
				var doingImage=1;

				function doNext()
				{
					doingSection++;
					if(doingSection<o.sections)
					{
						$("#p"+panelIDArray[doingSection]).fadeIn(o.sectionTransitionDelay,doNext);
					}
					else
					{
						if(doingImage == 0 && o.repeat) $("img:last", obj).hide(); // If doingImage = 0 and we're repeating, hide last (top) image
						$("img:eq("+doingImage+")", obj).show();
						$("div.section", obj).hide(); // Now hide all the divs so we can change their image
						doingSection=0;
						doingImage++;
						$("div.section", obj).css({'background-image':'url('+$("img:eq("+doingImage+")", obj).attr("src")+')'});
						if(doingImage < imgArray.length) // need to stop when doingImage equals imgArray.length
						{
							setTimeout(function(){$("#p"+panelIDArray[0]).fadeIn(o.sectionTransitionDelay,doNext)},o.imageTransitionDelay);
						}
						else if(o.repeat)
						{
							doingImage = 0;
							$("img:not(:last)", obj).hide(); // Hides all images in the container except the last one
							$("div.section", obj).hide();
							$("div.section", obj).css({'background-image':'url('+$("img:eq(0)", obj).attr("src")+')'});
							setTimeout(function(){$("#p"+panelIDArray[0]).fadeIn(o.sectionTransitionDelay,doNext)},o.imageTransitionDelay);							
						}
					}
				}
				setTimeout(function(){$("#p"+panelIDArray[0]).fadeIn(o.sectionTransitionDelay,doNext)},o.startDelay); // Kickoff the sequence
  		});
    	}
	});
})(jQuery);


