// navbar sidenav
function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}


$(document).ready(function () {

    $("#clients").owlCarousel({

        navigation: false, // Show next and prev buttons
        autoplay: true,
        slideSpeed: 300,
        paginationSpeed: 400,
        autoHeight: true,
        itemsCustom: [
            [0, 1],
            [450, 2],
            [600, 2],
            [700, 2],
            [1000, 4],
            [1200, 5],
            [1400, 5],
            [1600, 5]
        ],
    });

    $("#testimonial").owlCarousel({
        navigation: false, // Show next and prev buttons
        slideSpeed: 300,
        paginationSpeed: 400,
        singleItem: true
    });

});