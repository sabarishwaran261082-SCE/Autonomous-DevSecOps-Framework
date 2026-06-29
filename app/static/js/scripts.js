// ===============================
// Typing Animation
// ===============================

const text = [
    "AI Powered DevSecOps",
    "Autonomous Security Pipeline",
    "Cloud Native Deployment",
    "Intelligent Risk Assessment"
];

let index = 0;
let char = 0;

const typing = document.getElementById("typing");

function typeEffect(){

    if(!typing) return;

    if(char < text[index].length){

        typing.innerHTML += text[index].charAt(char);

        char++;

        setTimeout(typeEffect,80);

    }

    else{

        setTimeout(eraseEffect,1800);

    }

}

function eraseEffect(){

    if(char>0){

        typing.innerHTML=text[index].substring(0,char-1);

        char--;

        setTimeout(eraseEffect,40);

    }

    else{

        index++;

        if(index>=text.length)
            index=0;

        setTimeout(typeEffect,300);

    }

}

window.onload=typeEffect;

// ===============================
// Counter Animation
// ===============================

const counters=document.querySelectorAll(".counter");

counters.forEach(counter=>{

    counter.innerText="0";

    const updateCounter=()=>{

        const target=+counter.getAttribute("data-target");

        const c=+counter.innerText;

        const increment=target/100;

        if(c<target){

            counter.innerText=Math.ceil(c+increment);

            setTimeout(updateCounter,20);

        }

        else{

            counter.innerText=target;

        }

    };

    updateCounter();

});

// ===============================
// Scroll Reveal
// ===============================

const reveal=document.querySelectorAll(".card,.tech-grid div,.stats-card");

window.addEventListener("scroll",()=>{

    reveal.forEach(item=>{

        const top=item.getBoundingClientRect().top;

        if(top<window.innerHeight-100){

            item.classList.add("active");

        }

    });

});