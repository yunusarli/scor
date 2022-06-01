const parca_button = document.querySelector(".parca_kodu_update");
const saha_listesi = document.querySelector(".saha_listesi_update");

parca_button.addEventListener("click",()=>{
    update("update-parca-kodu/");
})

saha_listesi.addEventListener("click",()=>{
    update("update-saha-listesi/");
})

function update(link){
    fetch(link)
    .then(response => response.json())
    .then(data => console.log(data))
}