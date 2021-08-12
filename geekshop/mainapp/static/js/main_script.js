$( document ).on( 'click', '.block a', function(event) {
   if (this.hasAttribute('href')) {
       var link = this.href + '/ajax/';
       var link_array = link.split('/');
       if (link_array[4] === 'product') {
           $.ajax({
               url: link,
               success: function (data) {
                   $('.details').html(data.result);
               },
           });

           event.preventDefault();
       }
   }
});