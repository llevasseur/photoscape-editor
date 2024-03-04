// URL component
import React, { useState } from 'react'
import Button from './Button'
import axios from 'axios'
import './Form.css'

const URLInput = () => {
  const [url, setUrl] = useState('')
  const [choice, setChoice] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleURLInput = (event) => {
    setUrl(event.target.value)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    // Check if URL is not empty
    if (!url.trim()) {
      setErrorMessage('URL is required.')
      return
    }

    // Check if URL starts with the specified prefix
    if (!url.startsWith('https://www.espn.com/nhl/game/_/gameId')) {
      setErrorMessage('Invalid URL. Please enter a valid ESPN NHL game URL.')
      return
    }

    if (choice !== '') {
      setErrorMessage('')
      setLoading(true)
      // Send to API
      setTimeout(async () => {
        try {
          // Make an HTTP POST request to the Flask backend endpoint
          const response = await axios.post(
            'http://127.0.0.1:5000/process-url',
            {
              url: url,
              choice: choice,
            }
          )

          if (response.status === 200) {
            console.log(`REACHED 200, date_file: ${response.data.date_file}`)
            setErrorMessage(
              `Created ${choice} in Documents/NT/games/${response.data.date_file}`
            )
          } else {
            console.log('ERROR or no 200')
            setErrorMessage(
              `Error occurred while processing URL. Status Code ${response.status}.`
            )
          }
        } catch (error) {
          setErrorMessage(error.message)
        } finally {
          setLoading(false)
        }
      }, 500)
    } else {
      setErrorMessage('Please select an option.')
    }
  }

  return (
    <div>
      <div className="select-wrapper">
        <Button
          id="game-day"
          setChoice={setChoice}
          backgroundImages={['./game-day.png']}
          className="single-image-button"
          choice={choice}
        />
        <Button
          id="final-score"
          setChoice={setChoice}
          backgroundImages={['./final-score.png']}
          className="single-image-button"
          choice={choice}
        />
        <Button
          id="box-score"
          setChoice={setChoice}
          backgroundImages={['./box-score.png']}
          className="single-image-button"
          choice={choice}
        />
        <Button
          id="final-full"
          setChoice={setChoice}
          backgroundImages={['./box-score.png', './final-score.png']}
          className="double-image-button"
          choice={choice}
        />
      </div>
      <form className="custom-form">
        <div>
          <input
            className="url-bar"
            type="text"
            placeholder="Enter URL"
            value={url}
            onChange={handleURLInput}
          />
        </div>
        <div className="submit-container">
          {loading ? (
            <div className="loading-container">
              {loading && <div className="loading-animation"></div>}
            </div>
          ) : (
            <p
              className={`error-message ${errorMessage ? 'show' : ''}`}
              style={{ height: errorMessage ? 'auto' : '19px' }}
            >
              {errorMessage}
            </p>
          )}
          <button
            className="submit-button clickable"
            type="submit"
            onClick={handleSubmit}
            disabled={loading} // Disable button while loading
          >
            <span>SUB</span>
            <span>MIT</span>
          </button>
        </div>
      </form>
    </div>
  )
}

export default URLInput
