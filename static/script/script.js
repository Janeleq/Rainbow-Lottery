const randomone = document.getElementById('num-one');
const randomtwo = document.getElementById('num-two');
const randomthree = document.getElementById('num-three');
const randomfour = document.getElementById('num-four');
const btn = document.getElementById('btn');

btn.addEventListener('click', function(){
        numberone();
        numbertwo();
        numberthree();
        numberfour();
})



function numberone(){
    randomone.value = Math.floor(Math.random() * 10);
}

function numbertwo(){
    randomtwo.value = Math.floor(Math.random() * 10);
}

function numberthree(){
    randomthree.value = (Math.floor(Math.random() * 10));
}

function numberfour(){
    randomfour.value = Math.floor(Math.random() * 10);
}