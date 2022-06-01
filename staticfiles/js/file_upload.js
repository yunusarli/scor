// Dosya yükleme işlemlerini gerçekleştiren js dosyası

document.addEventListener('click',(element)=>{
    if (hasClass(element,"envanter_upload")){
        uploadFile(element,"envanter");
    }else if (hasClass(element,"eht_seri_upload")){
        uploadFile(element,"eht_seri")

    }else if (hasClass(element,"eht_sarf_upload")){
        uploadFile(element,"eht_sarf")
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
        console.log(data)
    })
}