(function(l) {
    l(document).on("ready", function() {
        var e = l("html")
          , s = new Image
          , o = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
        function t(e, s) {
            if (document.querySelector(e) != null) {
                l(".shipping-result").html(l(".page-simula-frete"));
                return
            } else {
                setTimeout(function() {
                    t(e, s)
                }, s)
            }
        }
        l(".botao-simular-frete, #shippingSimulatorButton").on("click", function() {
            l(".shipping-result").html("");
            t(".page-simula-frete", 1e3)
        });
        if (l.fn.jquery != "1.6.2") {
            l(".banner-home-slide").slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                prevArrow: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="165.116 0 369.767 700" width="50" height="50" class="slick-arrow arrow-prev"><path d="M170.965,363.918l330.214,330.214c3.814,3.961,8.948,5.868,13.937,5.868c4.987,0,10.122-2.054,13.936-5.868c7.775-7.774,7.775-20.244,0-28.019L212.92,349.981L529.051,33.85c7.775-7.775,7.775-20.244,0-28.019\tc-7.774-7.775-20.244-7.775-28.019,0L170.819,336.045C163.19,343.674,163.19,356.289,170.965,363.918z"/></svg>',
                nextArrow: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="165.116 0 369.767 700" width="50" height="50" class="slick-arrow arrow-next"><path d="M529.18,336.045L198.966,5.831c-7.774-7.775-20.244-7.775-28.019,0c-7.775,7.775-7.775,20.244,0,28.019l316.131,316.131L170.948,666.113c-7.775,7.774-7.775,20.244,0,28.019c3.813,3.814,8.948,5.868,13.936,5.868c4.988,0,10.122-1.907,13.937-5.868l330.214-330.214C536.809,356.289,536.809,343.674,529.18,336.045z"/></svg>',
                responsive: [{
                    breakpoint: 768,
                    settings: {
                        arrows: false
                    }
                }]
            });
            l(".showcase.s-carousel .product-list").slick({
                lazyLoad: "ondemand",
                slidesToShow: 4,
                slidesToScroll: 4,
                responsive: [{
                    breakpoint: 922,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3
                    }
                }, {
                    breakpoint: 767,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2,
                        arrows: false,
                        dots: true
                    }
                }]
            });
            l(".slider-for").slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                arrows: false,
                fade: true,
                asNavFor: ".slider-nav"
            });
            l(".slider-nav").slick({
                slidesToShow: 3,
                slidesToScroll: 1,
                asNavFor: ".slider-for",
                dots: false,
                arrows: true,
                focusOnSelect: true,
                responsive: [{
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1
                    }
                }]
            })
        }
        if (l(".caixa-cupom").length) {
            l(".caixa-cupom").parents("tr").addClass("cupom-wrapper")
        }
        if (l("#calculoFrete").length) {
            l("#calculoFrete").parents("tr").addClass("frete-wrapper")
        }
        l(".open-filters").on("click", function() {
            l(".filters-list").slideToggle()
        })
    });
    var e = l(".floating");
    l(window).on("scroll", function() {
        if (l(window).scrollTop() > 212) {
            e.addClass("fixed")
        } else {
            e.removeClass("fixed")
        }
    });
    l(".modal-login").on("click", function(e) {
        e.preventDefault();
        l("tray-login").show()
    })
}
)(jQuery);
(function() {
    var e = document.getElementsByClassName("trigger-menu")[0];
    var s = document.getElementsByTagName("html")[0];
    var o = document.getElementsByClassName("menu-mobile-backdrop")[0];
    e.addEventListener("click", function() {
        s.classList.add("menu-open")
    });
    s.addEventListener("click", function(e) {
        if (e.target == o) {
            this.className = this.className.replace(new RegExp("(^|\\b)" + "menu-open".split(" ").join("|") + "(\\b|$)","gi"), " ")
        }
    })
}
)();

function addCart(dataProductId){
    var dataSession = jQuery("html").attr("data-session");
    jQuery.ajax({
        method: "POST",
        url: "/web_api/cart/",
        contentType: "application/json; charset=utf-8",
        data: '{"Cart":{"session_id":"'+dataSession+'","product_id":"'+dataProductId+'","quantity":"1"}}'
    }).done(function( response, textStatus, jqXHR ) {
        window.location.href = response.cart_url;
    }).fail(function( jqXHR, status, errorThrown ){
        var response = jQuery.parseJSON( jqXHR.responseText );
        console.log(response);
    });
}