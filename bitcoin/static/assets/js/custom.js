/**
 * Index for Custom.js
 * Author: bPlugins
 * Date: 2024-July-06
 * ***************************************
 * Table of Contents
 * ***************************************
 * 01. Preloader and All after loader
 * 02. scroll top specific
 * 03. header-style
 * 04. mobile menu
 * 05. wow animation
 * 06. odometer
 * 07. fancybox/ligntbox
 * 08. custom tab
 * 09. accordion
 * 10. two-item-carousel
 * 11. three-item-carousel
 * 12. five-item-carousel
 * 13. nice select
 * 14. parallax icon
 * 15. round-circle
 */
(function ($) {
  "use strict";

  // 01. Preloader and All after loader
  function handlePreloader() {
    if ($(".loader-wrap").length) {
      $(".loader-wrap").delay(1000).fadeOut(500);
    }
  }

  // 02. scroll top specific
  if ($(".scroll-to-target").length) {
    $(".scroll-to-target").on("click", function () {
      var target = $(this).attr("data-target");
      // animate
      $("html, body").animate(
        {
          scrollTop: $(target).offset().top,
        },
        10
      );
    });
  }

  // 03. header-style
  function headerStyle() {
    if ($(".main-header").length) {
      var windowpos = $(window).scrollTop();
      var siteHeader = $(".main-header");
      var scrollLink = $(".scroll-top");
      if (windowpos >= 110) {
        siteHeader.addClass("fixed-header");
        scrollLink.addClass("open");
      } else {
        siteHeader.removeClass("fixed-header");
        scrollLink.removeClass("open");
      }
    }
  }

  headerStyle();

  // submenu
  if ($(".main-header li.dropdown ul").length) {
    $(".main-header .navigation li.dropdown").append(
      '<div class="dropdown-btn"><span class="fas fa-angle-down"></span></div>'
    );
  }

  // 04. mobile menu
  if ($(".mobile-menu").length) {
    var mobileMenuContent = $(".main-header .menu-area .main-menu").html();
    $(".mobile-menu .menu-box .menu-outer").append(mobileMenuContent);
    $(".sticky-header .main-menu").append(mobileMenuContent);

    //Dropdown Button
    $(".mobile-menu li.dropdown .dropdown-btn").on("click", function () {
      $(this).toggleClass("open");
      $(this).prev("ul").slideToggle(500);
    });
    //Dropdown Button
    $(".mobile-menu li.dropdown .dropdown-btn").on("click", function () {
      $(this).prev(".megamenu").slideToggle(900);
    });
    //Menu Toggle Btn
    $(".mobile-nav-toggler").on("click", function () {
      $("body").addClass("mobile-menu-visible");
    });

    //Menu Toggle Btn
    $(".mobile-menu .menu-backdrop,.mobile-menu .close-btn").on(
      "click",
      function () {
        $("body").removeClass("mobile-menu-visible");
      }
    );
  }

  // 05. wow animation
  if ($(".wow").length) {
    var wow = new WOW({
      mobile: false,
    });
    wow.init();
  }

  // 06. odometer
  if ($(".odometer").length) {
    var odo = $(".odometer");
    odo.each(function () {
      $(this).appear(function () {
        var countNumber = $(this).attr("data-count");
        $(this).html(countNumber);
      });
    });
  }

  // 07. fancybox/ligntbox
  if ($(".lightbox-image").length) {
    $(".lightbox-image").fancybox({
      openEffect: "fade",
      closeEffect: "fade",
      helpers: {
        media: {},
      },
    });
  }

  // 08. custom tab
  if ($(".tabs-box").length) {
    $(".tabs-box .tab-buttons .tab-btn").on("click", function (e) {
      e.preventDefault();
      var target = $($(this).attr("data-tab"));

      if ($(target).is(":visible")) {
        return false;
      } else {
        target
          .parents(".tabs-box")
          .find(".tab-buttons")
          .find(".tab-btn")
          .removeClass("active-btn");
        $(this).addClass("active-btn");
        target
          .parents(".tabs-box")
          .find(".tabs-content")
          .find(".tab")
          .fadeOut(0);
        target
          .parents(".tabs-box")
          .find(".tabs-content")
          .find(".tab")
          .removeClass("active-tab");
        $(target).fadeIn(100);
        $(target).addClass("active-tab");
      }
    });
  }

  // 09. accordion
  if ($(".accordion-box").length) {
    $(".accordion-box").on("click", ".acc-btn", function () {
      var outerBox = $(this).parents(".accordion-box");
      var target = $(this).parents(".accordion");

      if ($(this).hasClass("active") !== true) {
        $(outerBox).find(".accordion .acc-btn").removeClass("active");
      }

      if ($(this).next(".acc-content").is(":visible")) {
        return false;
      } else {
        $(this).addClass("active");
        $(outerBox).children(".accordion").removeClass("active-block");
        $(outerBox).find(".accordion").children(".acc-content").slideUp(300);
        target.addClass("active-block");
        $(this).next(".acc-content").slideDown(300);
      }
    });
  }

  // 10. two-item-carousel
  if ($(".two-item-carousel").length) {
    $(".two-item-carousel").owlCarousel({
      loop: true,
      margin: 30,
      nav: true,
      smartSpeed: 500,
      autoplay: 1000,
      navText: [
        '<span class="icon-9"></span>',
        '<span class="icon-10"></span>',
      ],
      responsive: {
        0: {
          items: 1,
        },
        480: {
          items: 1,
        },
        600: {
          items: 1,
        },
        800: {
          items: 2,
        },
        1200: {
          items: 2,
        },
      },
    });
  }

  // 11. three-item-carousel
  if ($(".three-item-carousel").length) {
    $(".three-item-carousel").owlCarousel({
      loop: true,
      margin: 30,
      nav: true,
      smartSpeed: 500,
      autoplay: 1000,
      navText: [
        '<span class="icon-9"></span>',
        '<span class="icon-10"></span>',
      ],
      responsive: {
        0: {
          items: 1,
        },
        480: {
          items: 1,
        },
        600: {
          items: 2,
        },
        800: {
          items: 2,
        },
        1200: {
          items: 3,
        },
      },
    });
  }

  // 12. five-item-carousel
  if ($(".five-item-carousel").length) {
    $(".five-item-carousel").owlCarousel({
      loop: true,
      margin: 30,
      nav: true,
      smartSpeed: 500,
      autoplay: 1000,
      navText: [
        '<span class="icon-28"></span>',
        '<span class="icon-29"></span>',
      ],
      responsive: {
        0: {
          items: 1,
        },
        480: {
          items: 2,
        },
        600: {
          items: 3,
        },
        800: {
          items: 4,
        },
        1200: {
          items: 5,
        },
      },
    });
  }

  // 13. nice select
  $(document).ready(function () {
    $("select:not(.ignore)").niceSelect();
  });

  // 14. parallax icon
  if ($(".parallax-scene-1").length) {
    var scene = $(".parallax-scene-1").get(0);
    var parallaxInstance = new Parallax(scene);
  }
  if ($(".parallax-scene-2").length) {
    var scene = $(".parallax-scene-2").get(0);
    var parallaxInstance = new Parallax(scene);
  }
  if ($(".parallax-scene-3").length) {
    var scene = $(".parallax-scene-3").get(0);
    var parallaxInstance = new Parallax(scene);
  }

  // 15. round-circle
  function roundcircle() {
    var rounderContainer = $(".piechart");
    if (rounderContainer.length) {
      rounderContainer.each(function () {
        var Self = $(this);
        var value = Self.data("value");
        var size = Self.parent().width();
        var color = Self.data("fg-color");

        Self.find("span").each(function () {
          var expertCount = $(this);
          expertCount.appear(function () {
            expertCount.countTo({
              from: 1,
              to: value * 100,
              speed: 3000,
            });
          });
        });
        Self.appear(function () {
          Self.circleProgress({
            value: value,
            size: 140,
            thickness: 10,
            emptyFill: "rgba(222,255,16,0.1)",
            animation: {
              duration: 3000,
            },
            fill: {
              color: color,
            },
          });
        });
      });
    }
  }

  jQuery(document).on("ready", function () {
    (function ($) {})(jQuery);
  });

  $(window).on("scroll", function () {
    headerStyle();
  });

  $(window).on("load", function () {
    handlePreloader();
    roundcircle();
  });
})(window.jQuery);
