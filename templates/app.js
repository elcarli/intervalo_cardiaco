$(document).ready(function(){
	
	var resp = "";
	var nombre=document.getElementById("nombre").value; 
	
    $('#empezar').click(function() {
		
		var intr = setInterval(function() {
			
			getSensor();
			
			$('#detener').click(function() {
				clearInterval(intr)
				});
			}, 1000)
			
	});
    
    
    function getSensor(){ 
		$.ajax({
                type: "GET",
                url: "/sesion?name="+nombre,
                success: function(data) {
						
                        var obj=data;
                        resp+="<p> HR: "+obj.hr+"</p> <p> RR: "+obj.rr+"</p> <br>";
                        $("#res").html(resp);
                }
            });
    }
});