(function() {
  'use strict';

  var items = document.querySelectorAll(".timeline li:not(.era-marker)");

  var observer = new IntersectionObserver(function(entries, observer) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting || entry.boundingClientRect.top < 0) {
        entry.target.classList.add("in-view");
        observer.unobserve(entry.target);
      }
    });
  }, {
    rootMargin: "0px 0px -5% 0px"
  });

  items.forEach(function(item) {
    observer.observe(item);
  });

})();

$(document).ready(function() {
  $('.image-link').magnificPopup({type:'image'});

  $('.one').click(function(){
    $('.frame').fadeIn();
  });
  
  $('.close').click(function(){
    $('.frame').fadeOut();
  });

  $(document).mouseup(function (e) {
    var container = $('.frame');
    if (!container.is(e.target) 
        && container.has(e.target).length === 0)
    {
        container.fadeOut();
    }
  });
});
