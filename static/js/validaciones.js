var eliminado ;
function cambiarRuta(ruta) {
    f = document.getElementById("validar");
    f.action=ruta;
    if (ruta=="eliminarestudiante"){
        eliminado=true;
    }
}
function cambiarRutaE(ruta) {
    e = document.getElementById("estudiante");
    e.action=ruta;
}
function comfirmarborrado() {
    if (eliminado){
        let r =confirm("desea eliminar el registro");
        return r; 
    }
    return true;
    
}