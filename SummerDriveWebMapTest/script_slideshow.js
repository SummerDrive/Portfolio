 // プラグインを登録
FilePond.registerPlugin(FilePondPluginFileValidateType);

const uploadField = document.querySelector('input[type="file"]');

var pond = FilePond.create(uploadField, {
  storeAsFile: true,
  allowMultiple: true,
  maxFiles: null,
  allowRemove: false,
  acceptedFileTypes: [
    'image/gif',
    'image/png',
    'image/jpeg'
  ]
});

//const files = pond.getFiles();
//console.log(typeof(files[0]));

const target = '.splide';
  
const options = {
  autoplay: true,
  interval: 10000,
  speed: 1000,
  pauseOnFocus: false,
  type: 'loop'
}
 
const mySplide = new Splide(target, options);

mySplide.mount();

// Splide初期化
//const splide = new Splide('#image-slider', {
//  type: 'loop',
//  perPage: 3,
//});
//splide.mount();

// ファイル追加時イベント
pond.on('addfile', (error, fileItem) => {
  if (error) return;

  // Blob URL生成
  const file = fileItem.file;
  const imageUrl = URL.createObjectURL(file);

  // スライド要素作成
  const li = document.createElement('li');
  li.classList.add('splide__slide');

  const img = document.createElement('img');
  img.src = imageUrl;
  img.style.height = '100%';

  li.appendChild(img);

  // Splideに追加
  mySplide.add(li);
});