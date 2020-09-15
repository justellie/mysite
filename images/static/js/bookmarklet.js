(function()
    {
        var jquery_version='3.4.1';
        var site_url='https://127.0.0.1:8000/';
        var static_url=site_url+'static/';
        var min_width=100;
        var min_height=100;
    
        function bookmarklet(msg)
            {
                // load CSS 
                var css=jQuery('<link>');
                css.attr({
                    rel:'stylesheet',
                    type:'text/css',
                    href:static_url+'css/bookmarklet.css?r='+Math.floor(Math.random()*99999999999999999999)
                });
                jQuery('head').append(css)
                //load HTML
                box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
                jQuery('body').append(box_html);

                //close event
                jQuery('#bookmarklet #close').click(function()
                {
                    jQuery('#bookmarklet').remove()
                });
                /*

                The next code uses the img[src$="jpg"] selector to find all <img> HTML
                    elements whose src attribute finishes with a jpg string. This means that you will
                    search all JPEG images displayed on the current website. You iterate over the
                    results using the each() method of jQuery. You add the images with a size larger
                    than the one specified with the min_width and min_height variables to your <div
                    class="images"> HTML container
                */
                jQuery.each(jQuery('img[src$="jpg"]'), function(index, image) {
                    if (jQuery(image).width() >= min_width && jQuery(image).height()
                    >= min_height)
                    {
                      image_url = jQuery(image).attr('src');
                      jQuery('#bookmarklet .images').append('<a href="#"><img src="'+image_url +'" /></a>');
                    }
                  });
                
                jQuery('#bookmarklet .images a').click(function(e){
                    selected_image = jQuery(this).children('img').attr('src');
                    // hide bookmarklet
                    jQuery('#bookmarklet').hide();
                    // open new window to submit the image
                    window.open(site_url +'images/create/?url='
                                + encodeURIComponent(selected_image)
                                + '&title='
                                + encodeURIComponent(jQuery('title').text()),
                                '_blank');
                  });
            };
        if(typeof window.jQuery!='undefined')
        {
            bookmarklet()
        }
        else
        {
            // Check for conflicts
            var conflict=typeof window.$ != 'undefined';
            //create the script and point to Google API
            var script=document.createElement('script');
            script.src='//ajax.googleapis.com/ajax/libs/jquery/'+jquery_version+'/jquery.min.js';
            // añadir el documento al head para procesamiento
            document.head.appendChild(script);
            // Create a way to wait until script loading
            var attempts=15;
            (function()
                {
                    //if jquery its undefine
                    if(typeof window.jQuery=='undefined')
                    {
                        if(--attempts>0)
                        {
                            // se llama  a si mismo en unos milisegundos
                            window.setTimeout(arguments.callee,250)
                        }
                        else
                        {
                            // Too much attempts to load, send error
                            alert('An error occurred while loading jQuery')
                        }
                    }
                    else
                    {
                        bookmarklet();
                    }
                })();
        }    
    })()