
//preview.js 

document.addEventListener('DOMContentLoaded', function(){
    //This file can be used to add interactive features to the resume preview

    //Print functionality
    const printButton = document.querySelector('button[onclick="window.print()"]');
    if(printButton){
        printButton.addEventListener('click', function(){
            window.print();
        });
    }
});