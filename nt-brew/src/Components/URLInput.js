// URL component
import React, { useState } from 'react'

const URLInput = () => {
    const [ url, setUrl ] = useState( '' )

    const handleInputChange = (event) => {
        setUrl(event.target.value)
    }

    const handleSubmit = (event) => {
        event.preventDefault()
        // Send to API
        console.log("TODO: Send to API")
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input 
                  type="text"
                  placeholder="Enter URL"
                  value={url}
                  onChange={handleInputChange}
                />
                <button type='submit'>Submit</button>
            </form>
        </div>
    )
}

export default URLInput