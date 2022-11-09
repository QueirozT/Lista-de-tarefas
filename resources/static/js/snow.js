neve();

function neve() {
  for (i = 1; i <= 198; i++){
    let snow = document.createElement('div');
    snow.classList.add('snow')
    
    document.querySelector('body').appendChild(snow)
  }  
}
