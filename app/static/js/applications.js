function animateElements() {
    const elements = document.querySelectorAll('h1, table');
    elements.forEach((el, index)=>{
        setTimeout(()=>{
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 200* index)
    });
}


window.addEventListener('load', animateElements)

document.addEventListener('DOMContentLoaded', (event)=>{
    const main = document.querySelector('main');
    let isScrolling;

    main.addEventListener('scroll', function (){
        window.clearTimeout(function () {
            console.log('Scroling has stoppped.')
        }, 66);
    }, false)
})