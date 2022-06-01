// Tab yapısı ile ilgili js dosyası
const tab_button = document.querySelector(".tab");
const table_button = document.querySelector(".table_button")

const tab_table = document.querySelector(".tab_table");

const table_for_real = document.querySelectorAll(".table_for_sayim");

tab_button.addEventListener("click",()=>{
    tab_table.style.display = "table";
    for (let element of table_for_real){
        element.style.display = "none";
    }
    
})

table_button.addEventListener("click",()=>{
    tab_table.style.display = "none";
    for (let element of table_for_real){
        element.style.display = "table";
    }
})