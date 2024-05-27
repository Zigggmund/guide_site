const grey_block = document.querySelector('.grey-block')
const admin_color = getComputedStyle(document.body).getPropertyValue('--admin-color')

grey_block.style.backgroundColor = admin_color;