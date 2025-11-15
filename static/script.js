const unitPhoto = document.getElementById("unitPhoto");
const caseNumberInput = document.getElementById("caseNumber");
const unitModelInput = document.getElementById("unitModel");
const serialNumberInput = document.getElementById("serialNumber");
const WOInput = document.getElementById("WO");
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

async function validateInfoUnitInputs() {
  const infoInputs = document.querySelectorAll('input[name="addInfo[]"]');
  const photoInputs = document.querySelectorAll('input[name="addPhoto[]"]');
  if (infoInputs.length < 1 && photoInputs.length < 1) return false;
  for (let input of infoInputs) {
    if (input.value.trim() === "") {
      let id = input.parentElement;
      let result = await Swal.fire({
        title: "Uups...",
        text: `Info foto dengan ID #${id.id} masih kosong. Apakah Anda ingin melengkapinya?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ya, lengkapi!",
        cancelButtonText: "Tidak, lanjutkan!",
        returnFocus: false,
      });
      if (result.isConfirmed) {
        input.focus();
        return false;
      } else continue;
    }
  }

  for (let input of photoInputs) {
    let id = input.parentElement;
    if (input.files.length === 0) {
      const result = await Swal.fire({
        title: "Error...",
        text: `Foto unit dengan ID #${id.id} masih kosong!`,
        icon: "error",
        confirmButtonText: "Oke",
        returnFocus: false,
      });
      if (result.isConfirmed) {
        input.focus();
        return false;
      }
    } else {
      let file = input.files[0];
      if (!file.type.startsWith("image/")) {
        let result = await Swal.fire({
          title: "Error...",
          text: `${file.name} bukan foto!`,
          icon: "error",
          confirmButtonText: "Oke",
          returnFocus: false,
        });
        if (result.isConfirmed) {
          input.focus();
          return false;
        }
      }
    }
  }
  return true;
}

document.addEventListener("DOMContentLoaded", () => {
  caseNumberInput.focus();
  submitButton.addEventListener("click", async (event) => {
    event.preventDefault();
    let caseNumber = caseNumberInput.value.trim();
    let unitModel = unitModelInput.value.trim();
    let serialNumber = serialNumberInput.value.trim();
    let WO = WOInput.files.length;
    if (caseNumber.length < 1) {
      Swal.fire({
        title: "Uups...",
        text: "Lengkapi data Case Number!",
        icon: "warning",
        confirmButtonText: "Oke",
        returnFocus: false,
      }).then((result) => {
        if (result.isConfirmed) {
          caseNumberInput.value = caseNumber;
          caseNumberInput.focus();
        }
      });
      return;
    }

    if (unitModel.length < 1) {
      Swal.fire({
        title: "Uups...",
        text: "Lengkapi data Unit Model!",
        icon: "warning",
        confirmButtonText: "Oke",
        returnFocus: false,
      }).then((result) => {
        if (result.isConfirmed) {
          unitModelInput.value = unitModel;
          unitModelInput.focus();
        }
      });
      return;
    }

    if (serialNumber.length < 1) {
      Swal.fire({
        title: "Uups...",
        text: "Lengkapi data Serial Number!",
        icon: "warning",
        confirmButtonText: "Oke",
        returnFocus: false,
      }).then((result) => {
        if (result.isConfirmed) {
          serialNumberInput.value = serialNumber;
          serialNumberInput.focus();
        }
      });
      return;
    }

    if (WO < 1) {
      Swal.fire({
        title: "Uups...",
        text: "Lengkapi data Foto Work Order!",
        icon: "warning",
        confirmButtonText: "Oke",
        returnFocus: false,
      }).then((result) => {
        if (result.isConfirmed) {
          WOInput.focus();
        }
      });
      return;
    }

    let = statusInfoUnitValidation = false;
    statusInfoUnitValidation = await validateInfoUnitInputs();
    if (statusInfoUnitValidation) document.getElementById("formPPT").submit();
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
    pId.classList = "text-secondary fst-italic text-end p-0 m-0 fs-12-px";
    pId.innerText = `#unitPhotoChild${counter}`;

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
    document.getElementById(id.dividerId).scrollIntoView({ block: "start" });
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
