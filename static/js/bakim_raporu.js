// Bakım Raporundaki satır işlemlerinin yürütüldüğü js dosyası

const add_satir = document.querySelector("#add_satir");
const delete_button = document.querySelector(".delete_satir_btn");
const save_button = document.querySelector(".btn-save");
const send_mail_button = document.querySelector(".send_email");


send_mail_button.addEventListener("click",()=>{
    const rapor_id = document.querySelector(".id").getAttribute("data-id")
    send_mail(rapor_id);
    console.log("clicked!")
})


save_button.addEventListener("click",()=>{
    let ids = document.getElementsByClassName("id_keeper")
    let counts = document.getElementsByClassName("count_keeper")
    let descriptions = document.getElementsByClassName("description_keeper")

    objects = []

    for (let i=0;i<ids.length;i++){
        obj = {}
        obj["id"] = ids[i].getAttribute("data-id")
        obj["sayim"] = counts[i].value
        obj["description"] = descriptions[i].value
        objects.push(obj) 
    }
    save(objects)
})


delete_button.addEventListener("click",()=>{
    const parca_kodu = document.querySelector("#silinecek_satir").value;
    const rapor_id = document.querySelector(".id").getAttribute("data-id")

    delete_satir(rapor_id,parca_kodu);
})

// Satir ekleme işlemi
add_satir.addEventListener("click",()=>{
    const parca_kodu = document.querySelector("#ad").value
    const parca_tanimi = document.querySelector("#soyad").value
    const quantity = document.querySelector("#yas").value
    const sayim = document.querySelector("#sayım").value
    const aciklama = document.querySelector("#açıklama").value
    const rapor_id = document.querySelector(".id").getAttribute("data-id")

    console.log(rapor_id)

    add(rapor_id,parca_kodu,parca_tanimi,quantity,sayim,aciklama)

})



function add(report_id,parca_kodu,parca_tanimi,quantity,sayim,aciklama){
    fetch("add/",{
        method:"POST",
        body:JSON.stringify({
            "report_id":report_id,
            "parca_kodu":parca_kodu,
            "parca_tanimi":parca_tanimi,
            "quantity":quantity,
            "sayim":sayim,
            "aciklama":aciklama,
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
}

function delete_satir(report_id,parca_kodu){
    fetch(`delete/${report_id}/${parca_kodu}/`,{
        method:"DELETE",
    })
    .then(response => response.json())
    .then(data => console.log(data))
}


function send_mail(rapor_id){
    fetch("send-mail/",{
        method:"POST",
        body:JSON.stringify({
            "report_id":rapor_id,
        })
    })
}

function save(objects){
    fetch(`save/`,{
        method:"POST",

        body:JSON.stringify({
            "objects":objects
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
}