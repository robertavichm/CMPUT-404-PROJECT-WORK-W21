$(document).ready(function(){

  // Making sure that we are already in a session
  if(localStorage.getItem("uuid") == null)
    window.location.href = host_url ;

  // And if we are already looged in
  // we cannot go back to login or register page
  if(localStorage.getItem("uuid") != null && window.location.pathname == "/" || window.location.pathname == "/login")
    window.location.href = host_url + '/home' ;


  // Logout
  $('.logout_btn').click(function(e) {
    console.log('logging out!')
    e.preventDefault();

    // empty localStorage
    localStorage.clear();

    // go back to login page
    window.location.href = host_url ;
  });
});
