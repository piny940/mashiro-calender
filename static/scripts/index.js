document.addEventListener('DOMContentLoaded', () => {
  const calendarFormEl = document.querySelector('#calendar-form')
  const submitButtonEl = document.querySelector('#create-calendar-button')

  submitButtonEl.addEventListener('click', () => {
    submitButtonEl.setAttribute('disabled', true)
    submitButtonEl.textContent = '処理中です。少々お待ちください。'
    calendarFormEl.submit()
  })
})
