(function($){
    
    $(document).on("ready",  function(){
        
        var html = $('html'),
            imgSrc = new Image(),
            windowWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
            
        // shipping added below cepbox
        function waitForElementToDisplay(selector, time) {
            if(document.querySelector(selector)!=null) {
                $('.shipping-result').html($('.page-simula-frete'));
                return;
            }
            else {
                setTimeout(function() {
                    waitForElementToDisplay(selector, time);
                }, time);
            }
        }
        
        $('.botao-simular-frete, #shippingSimulatorButton').on("click", function() {
            $('.shipping-result').html('');
            waitForElementToDisplay('.page-simula-frete', 1000);
        });
        
        if($.fn.jquery != '1.6.2'){
            
            $('.banner-home-slide').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                prevArrow: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="165.116 0 369.767 700" width="50" height="50" class="slick-arrow arrow-prev"><path d="M170.965,363.918l330.214,330.214c3.814,3.961,8.948,5.868,13.937,5.868c4.987,0,10.122-2.054,13.936-5.868c7.775-7.774,7.775-20.244,0-28.019L212.92,349.981L529.051,33.85c7.775-7.775,7.775-20.244,0-28.019	c-7.774-7.775-20.244-7.775-28.019,0L170.819,336.045C163.19,343.674,163.19,356.289,170.965,363.918z"/></svg>',
                nextArrow: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="165.116 0 369.767 700" width="50" height="50" class="slick-arrow arrow-next"><path d="M529.18,336.045L198.966,5.831c-7.774-7.775-20.244-7.775-28.019,0c-7.775,7.775-7.775,20.244,0,28.019l316.131,316.131L170.948,666.113c-7.775,7.774-7.775,20.244,0,28.019c3.813,3.814,8.948,5.868,13.936,5.868c4.988,0,10.122-1.907,13.937-5.868l330.214-330.214C536.809,356.289,536.809,343.674,529.18,336.045z"/></svg>',
    
                responsive: [{
                    breakpoint: 768,
                    settings: {
                        arrows: false
                    }
                }]
            });
            
            // start slick on products of home page
            $('.showcase.s-carousel .product-list').slick({
                lazyLoad: 'ondemand',
                slidesToShow: 4,
                slidesToScroll: 4,
                responsive: [
                    {
                        breakpoint: 922,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 3
                        }
                    },
                    {
                        breakpoint: 767,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 2,
                            arrows: false,
                            dots: true
                        }
                    }
                ]
            });
            
            // start slick on images of product on product page
            $('.slider-for').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                arrows: false,
                fade: true,
                asNavFor: '.slider-nav'
            });
            
            $('.slider-nav').slick({
                slidesToShow: 3,
                slidesToScroll: 1,
                asNavFor: '.slider-for',
                dots: false,
                arrows: true,
                focusOnSelect: true,
                responsive: [
                    {
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 1
                        }
                    }
                ]
            });            
        }
        
        // triggers to open and close menu mobile
        // $('.trigger-menu, .menu-mobile-backdrop').click(function(){
        //   html.addClass('menu-open'); 
        // });
        
        // $('.menu-mobile-backdrop,.backdrop-icon').click(function(){
        //   html.removeClass('menu-open'); 
        // });
        
        // cart support class
        if($('.caixa-cupom').length){
            $('.caixa-cupom').parents('tr').addClass('cupom-wrapper');
        }
        
        if($('#calculoFrete').length){
            $('#calculoFrete').parents('tr').addClass('frete-wrapper');
        }
        
        // open and close filters of smartfilter in catalog and search pages
        $('.open-filters').on("click", function() {
            $('.filters-list').slideToggle();
        });
    
    });
    
     //Topo flutuante
	var $fixedBar = $('.floating');
	$(window).on("scroll", function(){
		if($(window).scrollTop() > 212) {
			$fixedBar.addClass('fixed');
		} else {
			$fixedBar.removeClass('fixed');
		}
	});
	
    // modal login
    $('.modal-login').on("click", function(event) {
       event.preventDefault();
       $('tray-login').show();
    });		
    
})(jQuery);

// menu mobile
(function(){
    var btnMenu = document.getElementsByClassName('trigger-menu')[0];
    var html = document.getElementsByTagName('html')[0];
    var backdropMobile = document.getElementsByClassName('menu-mobile-backdrop')[0];

    btnMenu.addEventListener('touchend', function(){
        html.classList.add('menu-open');
    });

    html.addEventListener('touchend', function(e){
        if(e.target == backdropMobile){
            this.className = this.className.replace(new RegExp('(^|\\b)' + 'menu-open'.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
        }
    });
})();