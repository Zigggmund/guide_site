const grey_block = document.querySelector('.grey-block')
const moder_color = getComputedStyle(document.body).getPropertyValue('--admin-bright')
grey_block.style.backgroundColor = moder_color;

const title_main = getComputedStyle(document.body).getPropertyValue('--title-main')
grey_block.style.border = '3px solid ' + title_main;

