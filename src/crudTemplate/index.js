const URL = "http://127.0.0.1:5000/";

function cargarJuegos() {
  fetch(URL + "juegos")
    .then(function (response) {
      if (response.ok) {
        return response.json();
      }
    })
    .then(function (data) {
      let tablaJuegos = document.getElementById("tablaJuegos");
      tablaJuegos.innerHTML = "";

      for (let juego of data) {
        let fila = document.createElement("tr");
        fila.innerHTML = `
                        <td>${juego.codigo}</td>
                        <td>${juego.nombre}</td>
                        <td>${juego.descripcion}</td>
                        <td>${juego.participantes_min}</td>
                        <td>${juego.participantes_max}</td>
                        <td><img src=${juego.url_imagen} alt=${
          "imagen de " + juego.nombre
        } width=100 ></td>
                        <td>${juego.url_video}</td>
                        <td class="p-5">
                            <div class="d-flex flex-row align-self-stretch">
                                <button id=#editarModal class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#editarModal" data-juego-codigo=${
                                  juego.codigo
                                }>Editar</button>
                                <button class="btn btn-danger btn-sm" id="${
                                  juego.codigo
                                }" onclick="eliminarBtn(event)">Eliminar</button>
                            </div>
                        </td>
                    `;
        tablaJuegos.appendChild(fila);
      }
    })
    .catch(function (error) {
      alert("Error al obtener los juegos.");
      console.log(error.message);
    });
}

async function obtenerJuegoPorCodigo(codigo) {
  const res = await fetch(`${URL}/juegos/${codigo}`);
  return res.json();
}

function eliminarJuego(codigo) {
  if (confirm("¿Estás seguro de que quieres eliminar este juego?")) {
    fetch(URL + `juegos/${codigo}`, { method: "DELETE" })
      .then((response) => {
        if (response.ok) {
          alert("Juego eliminado correctamente.");
          cargarJuegos();
        }
      })
      .catch((error) => {
        alert(error.message);
      });
  }
}

function eliminarBtn(event) {
  const codigoJuego = Number(event.target.id);
  eliminarJuego(codigoJuego);
}

function cerrarSesion(){
  window.location.href = "/src/crudTemplate/login.html";
}

document.addEventListener("DOMContentLoaded", function () {
  cargarJuegos();

  const tableBody = document.querySelector("#juegosTable tbody");
  const agregarBtn = document.querySelector("#agregarBtn");
  const editarModal = document.querySelector("#editarModal");
  const modalTitle = document.querySelector("#modalTitle");
  const guardarBtn = document.querySelector("#guardarBtn");

  // Función para limpiar los campos del modal
  function limpiarCamposModal() {
    document.getElementById("editCodigo").value = "";
    document.getElementById("editTitulo").value = "";
    document.getElementById("editDescripcion").value = "";
    document.getElementById("editParticipantesMin").value = "";
    document.getElementById("editParticipantesMax").value = "";
    document.getElementById("editUrlImagen").value = "";
    document.getElementById("editUrlVideo").value = "";
  }

  editarModal.addEventListener("show.bs.modal", function (event) {
    const button = event.relatedTarget;

    if (button.getAttribute("data-juego-codigo")) {
      document.getElementById("editCodigolbl").style.display = "block"
      document.getElementById("editCodigo").style.display = "block"
      modalTitle.textContent = "Editar Juego";
      const juegoCodigo = button.getAttribute("data-juego-codigo");
      console.log(juegoCodigo);
      cargaEditarJuego(juegoCodigo);
    } else {
      document.getElementById("editCodigolbl").style.display = "none"
      document.getElementById("editCodigo").style.display = "none"
      modalTitle.textContent = "Agregar Juego";
      limpiarCamposModal();
    }
  });

  guardarBtn.addEventListener("click", () => {
    guardarCambios();
  });

  // Esta función se puede llamar para abrir el modal con datos específicos para editar
  async function cargaEditarJuego(codigo) {
    const juego = await obtenerJuegoPorCodigo(codigo);
    llenarCamposModal(juego);
  }

  function guardarJuego(formData) {
    fetch(URL + "juegos", {
      method: "POST",
      body: formData, // Aquí enviamos formData en lugar de JSON
    })
      .then(function (response) {
        if (response.ok) {
          alert("Juego guardado correctamente!");
          cargarJuegos();
          return response.json();
        }
      })
      .catch(function (error) {
        // Mostramos el error, y no limpiamos el form.
        alert("Error al agregar el Juego.");
      });
  }

  function editarJuego(codigo, formData) {
    fetch(URL + "juegos/" + codigo, {
      method: "PUT",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Juego actualizado correctamente");
        cargarJuegos();
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Error al actualizar el juego");
      });
  }

  function guardarCambios() {
    formData = new FormData();
    formData.append("nombre", document.getElementById("editTitulo").value);
    formData.append(
      "descripcion",
      document.getElementById("editDescripcion").value
    );
    formData.append(
      "urlImagen",
      document.getElementById("editUrlImagen").value
    );
    formData.append(
      "participantesMin",
      document.getElementById("editParticipantesMin").value
    );
    formData.append(
      "participantesMax",
      document.getElementById("editParticipantesMax").value
    );
    formData.append("urlVideo", document.getElementById("editUrlVideo").value);
    if (document.getElementById("editCodigo").value) {
      editarJuego(document.getElementById("editCodigo").value, formData);
    } else {
      guardarJuego(formData);
      limpiarCamposModal();
    }
  }

  function llenarCamposModal(juego) {
    document.getElementById("editCodigo").value = juego.codigo;
    document.getElementById("editTitulo").value = juego.nombre;
    document.getElementById("editDescripcion").value = juego.descripcion;
    document.getElementById("editParticipantesMin").value =
      juego.participantes_min;
    document.getElementById("editParticipantesMax").value =
      juego.participantes_max;
    document.getElementById("editUrlImagen").value = juego.url_imagen;
    document.getElementById("editUrlVideo").value = juego.url_video;
  }
});
