



// datatable
$(document).ready(function () {
  $('#customertable').DataTable({
      scrollY: 200,
      scrollX: true,
  });
});

$(document).ready(function () {
  $('#producttable').DataTable({
      scrollY: 200,
      scrollX: true,
      "ordering": false
  });
});

$(document).ready(function () {
  $('#sizetable').DataTable({
      scrollY: 200,
      scrollX: true,
      "ordering": false
  });
});

$(document).ready(function () {
  $('#coupontable').DataTable({
      scrollY: 200,
      scrollX: true,
  });
});


$(document).ready(function () {
  $('#categorytable').DataTable({
      scrollY: 200,
      scrollX: true,
      "ordering": false
  });
});

$(document).ready(function () {
  $('#ordertable').DataTable({
      scrollY: 200,
      scrollX: true,
  });
});


$(document).ready(function () {
  $('#orderitemtable').DataTable({
      scrollY: 200,
      scrollX: true,
  });
});

$(document).ready(function () {
  $('#coupontable').DataTable({
      scrollY: 200,
      scrollX: true,
  });
});

// Admin panel toggle

var el = document.getElementById("wrapper");
var toggleButton = document.getElementById("menu-toggle");

toggleButton.onclick = function () {
    el.classList.toggle("toggled");
};


