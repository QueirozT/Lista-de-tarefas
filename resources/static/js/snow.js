neve();

function neve() {
  for (i = 1; i <= 50; i++){
    let snow = document.createElement('div');
    snow.classList.add('snow')
    
    document.querySelector('body').appendChild(snow)
  }  
}
