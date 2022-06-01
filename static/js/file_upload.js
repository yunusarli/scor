// Dosya yükleme işlemlerini gerçekleştiren js dosyası

const popup = document.querySelector(".popup");
const close_popup = document.querySelector(".close_popup");
const message = document.querySelector(".message");


document.addEventListener('click',(element)=>{
    
    if (hasClass(element,"envanter_upload")){
        popup.style.display = "block";
        uploadFile(element,"envanter");
    }else if (hasClass(element,"eht_seri_upload")){
        popup.style.display = "block";
        uploadFile(element,"eht_seri")
    }else if (hasClass(element,"eht_sarf_upload")){
        popup.style.display = "block";
        uploadFile(element,"eht_sarf")
    }else if (hasClass(element,"sorgu_list")){
        uploadFile(element,"sorgu_list")
    }else if (hasClass(element,"rapor_referanslari")){
        uploadFile(element,"rapor_referanslari")
    }else if (hasClass(element,"close_popup")){
        popup.style.display = "none";
    }
    
})


function hasClass(elem,className){
    return elem.target.className.split(' ').indexOf(className) > -1
}

function uploadFile(element,type){
    const fileField = document.querySelector("#myFile")
    const formData = new FormData()
    console.log(element)
    formData.append("type",type)
    formData.append("file",fileField.files[0])

    fetch("upload/",{
        method:"POST",
        "body":formData
    })
    .then(response => response.json())
    .then(data => {
        popup.style.display = "none";
        message.innerHTML = data.message;
        message.style.display = "block";
        message.classList.add("alert-success");

    })
    .catch((error) =>{
        console.log(error);
        popup.style.display = "none";
        message.innerHTML = error;
        message.style.display = "block";
        message.classList.add("alert-danger");
    })
}
