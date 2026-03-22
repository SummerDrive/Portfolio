const target = '.splide';
  
const options = {
  autoplay: true,
  interval: 3000,
  speed: 1000,
  pauseOnFocus: false,
  type: 'loop'
}
 
const mySplide = new Splide(target, options);

mySplide.mount();