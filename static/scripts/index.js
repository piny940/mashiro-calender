document.addEventListener('DOMContentLoaded', () => {
  const calendarFormEl = document.querySelector('#calendar-form')
  const submitButtonEl = document.querySelector('#create-calendar-button')

  submitButtonEl.addEventListener('click', () => {
    submitButtonEl.setAttribute('disabled', true)
    submitButtonEl.textContent = '処理中です。少々お待ちください。'
    calendarFormEl.submit()
  })

  const addTweetForm = document.querySelector('#add-tweet-form')
  const addTweetButton = document.querySelector('#add-tweet-button')

  addTweetButton.addEventListener('click', () => {
    addTweetButton.setAttribute('disabled', true)
    addTweetButton.textContent = '処理中です。少々お待ちください。'
    addTweetForm.submit()
  })
})
