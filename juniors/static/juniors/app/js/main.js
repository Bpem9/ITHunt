$(function () {
  $('#defaultOpen').click()
  $('.cards-side__title').on('click', function () {
    let is_active = false

    if ($(this).hasClass('cards-side__title--active')) {
      is_active = true
    }

    $(this).removeClass('cards-side__title--active')

    if (!is_active) {
      $(this).addClass('cards-side__title--active')
    }
    // $(this).toggle()
  })
  // $('.btn-show').on('click',function(){
  //   $('.cards-side__hidden').toggle()
  // })
  $('.cards-content__sort').on('click', function () {
    if ($('.cards-content__hidden').hasClass('cards-content__hidden--active')) {
      $('.cards-content__hidden').removeClass('cards-content__hidden--active')
    } else {
      $('.cards-content__hidden').addClass('cards-content__hidden--active')
    }
  })
  $('.cards-content__hidden-link').on('click', function () {
    $('.cards-content__hidden').removeClass('cards-content__hidden--active')
    // console.log(1)
  })

  $('.cards-content__sort-text').on('click', function () {
    $(this).toggleClass('transform')
  })

  $('.profile__main-work__content-workedit__btn').on('click', function () {
    // console.log(1)
    $('.profile__main-work__content-workhidden').toggleClass('profile__main-work__content-workhidden--active')
  })
  $('.profile__main-work__content-eduedit__btn').on('click', function () {
    // console.log(1)
    $('.profile__main-work__content-eduhidden').toggleClass('profile__main-work__content-eduhidden--active')
  })
  let val1 = +$('#amount1').text()
  let val2 = +$('#amount2').text()
  // console.log(val1)
  $('#slider-range').slider({
    range: true,
    min: val1,
    max: val2,
    values: [val1, val2],
    slide: function (event, ui) {
      $('#amount1').text('€' + ui.values[0] + 'K')
      $('#amount2').text('€' + ui.values[1] + 'K')
    },
  })
  $('#amount').val('$' + $('#slider-range').slider('values', 0) + ' - $' + $('#slider-range').slider('values', 1))

  let dt = new AirDatepicker('#datepicker', {
    isMobile: true,
    altField: '#datefield',
    altFieldDateFormat: 'yyyy-MM-dd',
  })
  // console.log(dt)
})

let days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
let d = new Date()
let n = d.getDay()
let dayTime = days[n] + ','
// console.log(dayTime)
let date = new Date()
let month = date.getMonth()
let monthes = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
let number = date.getDate()
// if (number < 10) {
//   number = '0' + number
// }

let fullDate = dayTime + ' ' + number + ' ' + monthes[month]
console.log(fullDate)
$('.card-tabs__timepicker-title').text(fullDate)

$('.card-tabs__timepicker-list__item').on('click', function () {
  $(this).toggleClass('active')
})

function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName('tab-content')
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = 'none'
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName('tabs-link')
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(' active', '')
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = 'block'
  evt.target.className += ' active'
}
function openCardTab(evt, CardTabName) {
  // Declare all variables
  var i, tabcontent, tablinks

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName('card-tabs__content')
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = 'none'
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName('card-tabs__link')
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(' active', '')
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(CardTabName).style.display = 'block'
  evt.target.className += ' active'
}
