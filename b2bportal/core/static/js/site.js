 /* search JQuery */

// (function () {
//  $("#myInput").on("keyup", function() {
//    var value = $(this).val().toLowerCase();
//    $("#myList li").filter(function() {
//      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
//    });
//  });
//});

 /* search JQuery  */

  /* Cookie scribt */
  const cookieBox = document.querySelector(".wrapper"),
        blockbox = document.querySelector(".blockpage"),
        acceptBtn = cookieBox.querySelector("button");
    acceptBtn.onclick = () => {
        //setting cookie for 1 month, after one month it'll be expired automatically
        document.cookie = "CookieBy=NaqelExpress; path=/;max-age=" + 60 * 60 * 24 * 30;
        if (document.cookie) { //if cookie is set
            cookieBox.classList.add("hide"); //hide cookie box
            blockbox.classList.add("hide");
        } else { //if cookie not set then alert an error
            alert("Cookie can't be set! Please unblock this site from the cookie setting of your browser.");
        }
    }
    let checkCookie = document.cookie.indexOf("CookieBy=NaqelExpress"); //checking our cookie
    //if cookie is set then hide the cookie box else show it
    checkCookie != -1 ? cookieBox.classList.add("hide") : cookieBox.classList.remove("hide");
    checkCookie != -1 ? blockbox.classList.add("hide") : blockbox.classList.remove("hide");

  
/* Cookie script end  */




/* SUBSCRIBE SCRIBT */
// Submit post on submit
function SubscribeJs() {
    event.preventDefault();

    console.log("form submitted!")  // sanity check
    create_post();
};

function create_post() {
     var formData = new FormData();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    formData.append('csrfmiddlewaretoken', csrftoken);
    var Email = $("#post-text").val();
    formData.append('post-text', Email);
    console.log(formData);
    $.ajax({
        url : "ajax/create_post", // the endpoint
        type : "POST", // http method
        processData: false,
        contentType: false,
        data : formData, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            $("#subscribe-msg").prepend("Subscription Added");
            $("#subscribe-msg").addClass("cmt-btn text-white");
            $("#subscribe-msg").addClass(" bgnaqelred");
            setTimeout(function() {
            $('#subscribe-msg').fadeOut('fast');
            $("#subscribe-msg").removeClass("cmt-btn text-white");
            $("#subscribe-msg").removeClass("bgnaqelred");
        }, 5000);

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#post-text').val(''); // remove the value from the input
            $("#subscribe-msg").prepend("You are Already Subscribed");
            $("#subscribe-msg").addClass("cmt-btn text-white");
            $("#subscribe-msg").addClass("bgnaqelred");
            setTimeout(function() {
            $('#subscribe-msg').fadeOut('fast');
            $("#subscribe-msg").removeClass("cmt-btn text-white");
            $("#subscribe-msg").removeClass("bgnaqelred");
        }, 5000);
        }
    });
};


/* SUBSCRIBE SCRIBT END */


/* Chatbot Script *//* 
var eventMethod = window.addEventListener
    ? "addEventListener"
    : "attachEvent";
var eventer = window[eventMethod];
var messageEvent = eventMethod === "attachEvent"
    ? "onmessage"
    : "message";

eventer(messageEvent, function (e) {
    console.log(e);
    if (e.origin !== "https://d2ka5v04lnst0s.cloudfront.net") return;

    if (e.data.open == true) {
    // add class to show the full the cotainer
    document.getElementById("frameContainer").classList.add('chatbot-container');
    document.getElementById("").classList.remove('ar_lang_height');
    document.getElementById("frameContainer").classList.remove('en_lang_height');
    } 
    else if (e.data.close_welcome == true) {
      document.getElementById("frameContainer").classList.remove('ar_lang_height');
      document.getElementById("frameContainer").classList.remove('en_lang_height');
      document.getElementById("frameContainer").classList.add('normal-height');
    }
    else if (e.data.open == false) {
      // remove this class
      document.getElementById("frameContainer").classList.remove('chatbot-container');   
      document.getElementById("frameContainer").classList.add('normal-height');
    }
});

// please set the url of the iframe chatbot url
var url_string = document.getElementById("frameContainer").src; 
var url = new URL(url_string);
var show_welcome = url.searchParams.get("show_welcome");
var langauge = url.searchParams.get("lang");

if (show_welcome == "false") {
  document.getElementById("frameContainer").classList.add('normal-height');
} else { 
  if (langauge == "ar") {
    document.getElementById("frameContainer").classList.add('ar_lang_height');
  } else { document.getElementById("frameContainer").classList.add('en_lang_height'); }
}
 */
/* Charbot Script end */


 /* dropdown Ajax for cities */

	 $("#id_shipping_from_country").change(function () {
    var url = $("#pickupform").attr("data-cities-url");  // get the url of the `load_cities` view
    var countryId = $(this).val();  // get the selected country ID from the HTML input
    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      data: {
        'country': countryId       // add the country id to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#id_pickup_city").html(data);  // replace the contents of the city input with the data that came from the server
      }
    });
  });


  $("#id_shipping_to_country").change(function () {
    var url = $("#pickupform").attr("data-cities-url");  // get the url of the `load_cities` view
    var countryId = $(this).val();  // get the selected country ID from the HTML input
    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      data: {
        'country': countryId       // add the country id to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#id_shipping_to_city").html(data);  // replace the contents of the city input with the data that came from the server
      }
    });
  });

 /* dropdown Ajax for cities */


 /* more details tracking but */


 function myFunction(divid) {
  var spanx= document.getElementById(divid+"span");
  var spanless= document.getElementById(divid+"spanless");

  var x = document.getElementById(divid);
  $(x).toggle('slow');
  
}


 /* more details tracling */

 /* country code dropdown */

 	// Vanilla Javascript
//   var input = document.querySelector("#phone");
//   window.intlTelInput(input,({
//       // options here
//   }));
 
  $(document).ready(function() {
     $('.iti__flag-container').click(function() { 
       var countryCode = $('.iti__selected-flag').attr('title');
       var countryCode = countryCode.replace(/[^0-9]/g,'')
       $('#phone').val("");
       $('#phone').val("+"+countryCode+""+ $('#phone').val());
    });
 });

 /* country code dropdown */


// Reset button start
    function clearvalue()
    {
        document.getElementById('id_waybills').value = "";
    }
//Reset Button End
$(document).ready(function() {
var mobile = (/iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()));
if (mobile) {
    console.log('show')
    $('#mobilemodal').modal('show');
} else {
    //alert("NO MOBILE DEVICE DETECTED");
}
});


/* slides in tracking page */


$(function() {
    $('#myCarousel').carousel({interval: 2000});
    $('#myCarousel').on('slid', function() {
        var to_slide = $('.carousel-item.active').attr('data-slide-no');
        $('.myCarousel-target.active').removeClass('active');
        $('.carousel-indicators [data-slide-to=' + to_slide + ']').addClass('active');
    });
    $('.myCarousel-target').on('click', function() {
        $('#myCarousel').carousel(parseInt($(this).attr('data-slide-to')));
        $('.myCarousel-target.active').removeClass('active');
        $(this).addClass('active');
    });
});

/* slides in tracking page end */
