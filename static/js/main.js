function viz1()
{
    x_c_list = document.getElementById("viz1_x").value
    l_c_list = document.getElementById("viz1_l").value

    var xmlHttp = new XMLHttpRequest();
    var urlX = "/viz/viz1?x_c="+x_c_list+"&l_c="+l_c_list;

    xmlHttp.open( "GET", urlX, false );
    xmlHttp.send(null);

    html = xmlHttp.responseText

    var container = document.getElementById("viz1_container");
    container.contentWindow.document.open();
    container.contentWindow.document.write(html);
    container.contentWindow.document.close();


}


  

