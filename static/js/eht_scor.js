//eht verilerinin scor'a gönderilmesi

const scor_calistir = document.querySelector("#sonuc_rapor_olustur")

const saha_no = document.querySelector("#saha_no_hidden").value;
const message = document.querySelector(".message");

scor_calistir.addEventListener("click",()=>{
    eht_scor_calistir(saha_no);
})


function eht_scor_calistir(saha_no){
    let parca_listesi = []
    let parca_kodlari = document.getElementsByClassName("bold-blue");
    for (let parca of parca_kodlari){
        parca_kodu = parca.childNodes[4].innerText;
        parca_listesi.push(parca_kodu);
    }
    console.log(parca_listesi)
    fetch("scor-calistir/",{
        method:"POST",
        body:JSON.stringify({
            "saha_no":saha_no,
            "parca_kodlari":parca_listesi,
        })
    })
    .then(response => response.json())
    .then(data => {
        message.style.display = "block";
        message.innerText = data.message
    })
}