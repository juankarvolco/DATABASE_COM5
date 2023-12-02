const URL = "http://127.0.0.1:5000/" 
// Realizamos la solicitud GET al servidor para obtener todos los juegos 
fetch(URL + 'juegos') 
    .then(function (response) { 
        if (response.ok) { 
            return response.json(); 
        } 
    }) 
    .then(function (data) { 
        let tablaJuegos = document.getElementById('tablaJuegos'); 
        // Iteramos sobre los juegos y agregamos filas a la tabla 
        for (let juego of data) { 
            let fila = document.createElement('tr'); 
            fila.innerHTML = '<td>' + juego.id + '</td>' + '<td>' + juego.nombre + '</td>' + '<td>' + juego.descripcion + '</td>' + '<td>' + juego.urlImagen + '</td>' + '<td>' + juego.participantesMin + '</td>' + '<td>' + juego.participantesMax + '</td>' + '<td>' + juego.urlVideo + '</td>'; 
            tablaProductos.appendChild(fila); 
        } 
    }) 
    .catch(function (error) { 
        // Código para manejar errores 
        alert('Error al obtener los juegos.'); });