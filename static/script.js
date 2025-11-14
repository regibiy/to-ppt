const unitPhoto = document.getElementById("unitPhoto");
let caseNumberInput = document.getElementById("caseNumber");
let unitModelInput = document.getElementById("unitModel");
let serialNumberInput = document.getElementById("serialNumber");
const submitButton = document.getElementById("submitButton");

function previewImage(previewArea) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (e) {
    const preview = document.getElementById(previewArea);
    preview.src = e.target.result;
    preview.style.display = "block";
  };

  reader.readAsDataURL(file);
}

async function validateInfoInputs() {
  const infoInputs = document.querySelectorAll('input[name="addInfo[]"]');
  for (const input of infoInputs) {
    if (input.value.trim() === "") {
      const result = await Swal.fire({
        title: "Input masih kosong",
        text: "Mau isi dulu tidak?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Isi",
        cancelButtonText: "Lanjut",
        returnFocus: false,
      });

      if (result.isConfirmed) {
        input.focus();
        return false;
      } else if (result.isDenied) {
        continue;
      }
    }
  }
  return true;
}

document.addEventListener("DOMContentLoaded", () => {
  caseNumberInput.focus();
  submitButton.addEventListener("click", async (event) => {
    event.preventDefault();
    const valid = await validateInfoInputs();
    if (valid) alert("oke");

    // caseNumber = caseNumberInput.value.trim();
    // unitModel = unitModelInput.value.trim();
    // serialNumber = serialNumberInput.value.trim();
    // if (caseNumber.length < 1) {
    //   Swal.fire({
    //     title: "Uups...",
    //     text: "Lengkapi data Case Number!",
    //     icon: "warning",
    //     confirmButtonText: "Oke",
    //     returnFocus: false,
    //   }).then((result) => {
    //     if (result.isConfirmed) {
    //       caseNumberInput.value = caseNumber;
    //       caseNumberInput.focus();
    //     }
    //   });
    // } else if (unitModel.length < 1) {
    //   Swal.fire({
    //     title: "Uups...",
    //     text: "Lengkapi data Unit Model!",
    //     icon: "warning",
    //     confirmButtonText: "Oke",
    //     returnFocus: false,
    //   }).then((result) => {
    //     if (result.isConfirmed) {
    //       unitModelInput.value = unitModel;
    //       unitModelInput.focus();
    //     }
    //   });
    // } else {
    //   Swal.fire({
    //     title: "Uups...",
    //     text: "Lengkapi data Serial Number!",
    //     icon: "warning",
    //     confirmButtonText: "Oke",
    //     returnFocus: false,
    //   }).then((result) => {
    //     if (result.isConfirmed) {
    //       serialNumberInput.value = serialNumber;
    //       serialNumberInput.focus();
    //     }
    //   });
    // }
  });

  let counter = 0;

  function addImage() {
    counter++;

    const divider = document.createElement("div");
    divider.id = `unitPhotoChild${counter}`;
    divider.classList = "mb-3 border p-3 rounded";

    const labelInfo = document.createElement("label");
    labelInfo.htmlFor = `addInfo${counter}`;
    labelInfo.classList = "form-label";
    labelInfo.innerText = "Keterangan Foto";

    const inputInfo = document.createElement("input");
    inputInfo.type = "text";
    inputInfo.name = "addInfo[]";
    inputInfo.id = `addInfo${counter}`;
    inputInfo.classList = "form-control mb-3";

    const inputPhoto = document.createElement("input");
    inputPhoto.type = "file";
    inputPhoto.name = "addPhoto[]";
    inputPhoto.id = `addPhoto${counter}`;
    inputPhoto.accept = "image/*";
    inputPhoto.classList = "form-control mb-3";

    const previewPhoto = document.createElement("img");
    previewPhoto.src = "";
    previewPhoto.alt = "Preview Foto Unit";
    previewPhoto.id = `previewPhoto${counter}`;
    previewPhoto.width = 200;
    previewPhoto.height = 200;
    previewPhoto.classList = "img-thumbnail mb-3";

    const cancelButton = document.createElement("button");
    cancelButton.type = "button";
    cancelButton.id = `cancelButton${counter}`;
    cancelButton.innerText = "Hapus Foto Unit";
    cancelButton.classList = "btn btn-outline-danger";

    const pId = document.createElement("p");
    pId.classList = "text-secondary fst-italic text-end p-0 m-0 fs-12-custom";
    pId.innerText = `UnitPhotoID #${counter}`;

    divider.append(labelInfo, inputInfo, previewPhoto, inputPhoto, cancelButton, pId);
    unitPhoto.append(divider);

    inputPhoto.addEventListener("change", (event) => {
      previewImage(previewPhoto.id);
    });

    cancelButton.addEventListener("click", (event) => {
      divider.remove();
    });

    return { dividerId: divider.id, inputInfoId: inputInfo.id };
  }

  const addPhoto = document.getElementById("addPhoto");
  addPhoto.addEventListener("click", (event) => {
    let id = addImage();
    document.getElementById(id.inputInfoId).focus();
    document.getElementById(id.dividerId).scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });

  document.getElementById("WO").addEventListener("change", (event) => {
    let WO = document.getElementById("WO");
    for (let wo of WO.files) {
      if (!wo.type.startsWith("image/")) {
        Swal.fire({
          title: "Error...",
          text: `${wo.name} bukan foto!`,
          icon: "error",
          confirmButtonText: "Oke",
        }).then((result) => {
          if (result.isConfirmed) {
            WO.value = null;
            return;
          }
        });
      } else previewImage("previewWorkOrder");
    }
  });
});
