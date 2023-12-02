URL = "http://127.0.0.1:5000/" 

const app = Vue.createApp({ 
    data() { return { 
        id: '', 
        nombre: '', 
        descripcion: '', 
        urlImagen: '', 
        participantesMin: '', 
        participantesMax: '', 
        urlVideo: null,
        imagenUrlTemp: null, 
        mostrarDatosJuegos: false, 
    }; 
},
 methods: { 
    obtenerJuego() { 
        fetch(URL + 'juegos/' + this.id) 
        .then(response => response.json()) 
        .then(data => { 
            this.nombre = data.nombre; 
            this.descripcion = data.descripcion; 
            this.urlImagen = data.urlImagen; 
            this.participantesMin = data.participantesMin; 
            this.participantesMax = data.participantesMax;
            this.urlVideo = data.urlVideo;
            this.mostrarDatosJuego = true; 
        }) 
        .catch(error => console.error('Error:', error)); 
    }, 
    seleccionarImagen(event) { 
        const file = event.target.files[0]; 
        this.imagenSeleccionada = file; 
        this.imagenUrlTemp = URL.createObjectURL(file); // Crea una URL temporal para la vista previa
    },
        guardarCambios() { 
        const formData = new FormData(); 
        formData.append('id', this.id); 
        formData.append('nombre', this.nombre); 
        formData.append('descripcion', this.descripcion);
        formData.append('urlImagen', this.urlImagen); 
        formData.append('participantesMin', this.participantesMin); 
        formData.append('participantesMax', this.participantesMax);
        formData.append('urlVideo', this.urlVideo);
        if (this.imagenSeleccionada) { 
            formData.append('imagen', this.imagenSeleccionada, this.imagenSeleccionada.name); 
        } 
        
        fetch(URL + 'productos/' + this.id, { 
            method: 'PUT', 
            body: formData, 
        }) 
            .then(response => response.json()) 
            .then(data => { 
                alert('Juego actualizado correctamente'); 
                this.limpiarFormulario(); 
            }) 
            .catch(error => { 
                console.error('Error:', error); 
                alert('Error al actualizar el juego'); 
            }); 
        }, 
        limpiarFormulario() { 
            this.id = ''; 
            this.nombre = ''; 
            this.descripcion = ''; 
            this.urlImagen = ''; 
            this.participantesMin = ''; 
            this.participantesMax = '';
            this.urlVideo = '';
            this.imagenSeleccionada = null; 
            this.imagenUrlTemp = null; 
            this.mostrarDatosJuego = false; 
        } 
    } 
}); 

app.mount('#app');